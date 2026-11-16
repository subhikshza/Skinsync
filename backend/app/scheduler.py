"""Builds the 7-day AM/PM routine.

Idea in one line: basics go on every day; "active" products are placed one
day at a time, skipping any active that clashes with one already placed.
"""
from .engine import Catalog, detect_conflicts
from .models import Conflict, Day, PlanItem, Product, Routine, Step

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Layering order inside one routine: thinnest first, sunscreen last.
TYPE_ORDER = {"cleanser": 1, "toner": 2, "serum": 3, "treatment": 4,
              "moisturizer": 5, "sunscreen": 6}

# Where a product type normally goes when no rule says otherwise.
DEFAULT_SLOTS = {"cleanser": {"AM", "PM"}, "toner": {"AM", "PM"}, "serum": {"AM", "PM"},
                 "treatment": {"PM"}, "moisturizer": {"AM", "PM"}, "sunscreen": {"AM"}}

# Who gets first pick of a day when two actives are tied.
FAMILY_PRIORITY = ["retinoid", "aha", "bha", "benzoyl_peroxide", "vitamin_c"]


def build_week(products: list[Product], level: str, catalog: Catalog) -> Routine:
    conflicts = detect_conflicts(products, catalog)
    real = [c for c in conflicts if c.severity != "info"]      # conflicts that need action
    by_id = {p.id: p for p in products}
    warnings: list[str] = []
    reasons: dict[str, list[str]] = {p.id: [] for p in products}

    actives = [p for p in products if catalog.is_active(p)]
    basics = [p for p in products if not catalog.is_active(p)]

    def partners(pid: str) -> list[tuple[str, Conflict]]:
        """Products that pid has a real conflict with."""
        out = []
        for c in real:
            if c.product_a == pid:
                out.append((c.product_b, c))
            elif c.product_b == pid:
                out.append((c.product_a, c))
        return out

    # ---- Step 1: AM or PM for each active -------------------------------
    slot: dict[str, str] = {}
    allowed: dict[str, set] = {}
    for p in actives:
        slots = set(DEFAULT_SLOTS[p.type])
        for fam in catalog.families_of(p):
            rule = catalog.timing.get(fam)
            if rule:
                if not slots & set(rule.allowed_slots):
                    continue
                if slots != slots & set(rule.allowed_slots):
                    reasons[p.id].append(
                        f"{'Morning' if rule.allowed_slots == ['AM'] else 'Night'} only ({rule.id})")
                slots &= set(rule.allowed_slots)
        allowed[p.id] = slots

    # Actives with only one possible slot are fixed first.
    for p in sorted(actives, key=lambda p: (len(allowed[p.id]), p.id)):
        options = sorted(allowed[p.id])
        if len(options) == 1:
            slot[p.id] = options[0]
            continue
        # Flexible: pick the slot with fewer clashing products already in it.
        def clashes(s):
            return sum(1 for other, _ in partners(p.id) if slot.get(other) == s)
        slot[p.id] = min(options, key=lambda s: (clashes(s), s != "PM"))

    # ---- Step 2: which pairs of actives must not share a day -------------
    # (a) two clashing actives that ended up in the same slot
    # (b) any "separate_days" rule, even if they are in different slots
    blocked: dict[str, set] = {p.id: set() for p in actives}
    for c in real:
        a, b = c.product_a, c.product_b
        if a not in slot or b not in slot:
            continue                                   # one of them is a cleanser
        if slot[a] == slot[b] or c.resolution == "separate_days":
            blocked[a].add(b)
            blocked[b].add(a)
            c.resolved_how = "Used on different days."
            reasons[a].append(f"Not on the same day as {by_id[b].name} ({c.rule_id})")
            reasons[b].append(f"Not on the same day as {by_id[a].name} ({c.rule_id})")
        else:
            c.resolved_how = (f"Used in different routines: {by_id[a].name} in the {slot[a]}, "
                              f"{by_id[b].name} in the {slot[b]}.")

    # ---- Step 3: weekly limits for each active ---------------------------
    cap: dict[str, int] = {}
    no_consec: dict[str, bool] = {}
    for p in actives:
        rules = [catalog.timing[f] for f in catalog.families_of(p) if f in catalog.timing]
        cap[p.id] = min([r.max_days_per_week[level] for r in rules], default=7)
        no_consec[p.id] = any(r.no_consecutive_days[level] for r in rules)
        if cap[p.id] < 7:
            strict = min(rules, key=lambda r: r.max_days_per_week[level])
            reasons[p.id].append(f"At most {cap[p.id]} days a week at {level} level ({strict.id})")

    def priority(p: Product) -> int:
        fams = catalog.families_of(p)
        return min((FAMILY_PRIORITY.index(f) for f in fams if f in FAMILY_PRIORITY), default=99)

    # ---- Step 4: place actives day by day (greedy) -----------------------
    on: dict[str, list[int]] = {p.id: [] for p in actives}     # day numbers per active
    for d in range(7):
        today: list[str] = []
        # Fewest days so far goes first, so clashing actives take turns.
        for p in sorted(actives, key=lambda p: (len(on[p.id]), priority(p), p.id)):
            if len(on[p.id]) >= cap[p.id]:
                continue                               # weekly limit reached
            if no_consec[p.id] and (d - 1 in on[p.id] or (d == 6 and 0 in on[p.id])):
                continue                               # would be two days running
            if blocked[p.id] & set(today):
                continue                               # clashes with one already placed today
            today.append(p.id)
            on[p.id].append(d)

    for p in actives:
        if blocked[p.id] and len(on[p.id]) < min(cap[p.id], 3):
            warnings.append(
                f"{p.name} only fits on {len(on[p.id])} day(s) because it clashes with "
                "other products on your shelf. Consider using fewer strong actives.")

    # ---- Step 5: basics, with one special case for face washes ----------
    basic_slots: dict[str, set] = {p.id: set(DEFAULT_SLOTS[p.type]) for p in basics}
    # A face wash that truly clashes with an active (e.g. benzoyl peroxide wash +
    # retinol) is kept out of that active's routine.
    wash_clashes = [(wash, other, c) for c in real
                    for wash, other in ((c.product_a, c.product_b), (c.product_b, c.product_a))
                    if wash in basic_slots and other in slot]
    for wash, other, c in wash_clashes:                 # first remove every blocked slot
        basic_slots[wash].discard(slot[other])
    for wash, other, c in wash_clashes:                 # then describe the final result
        left = sorted(basic_slots[wash])
        if left:
            c.resolved_how = (f"{by_id[wash].name} is used only in the {left[0]}, "
                              f"away from {by_id[other].name}.")
            reasons[wash].append(f"{'Morning' if left[0] == 'AM' else 'Night'} only, "
                                 f"away from {by_id[other].name} ({c.rule_id})")
        else:
            c.resolved_how = (f"{by_id[wash].name} clashes with products in both routines, "
                              "so it was left out of the plan.")
            reasons[wash].append(f"Left out: clashes with {by_id[other].name} ({c.rule_id})")
    for wash in {w for w, _, _ in wash_clashes if not basic_slots[w]}:
        warnings.append(f"{by_id[wash].name} clashes with products in both your morning and "
                        "night routines, so it is not in the plan. Remove one of the clashing "
                        "products if you want to use it.")

    # ---- Step 6: build the 7 days in layering order ----------------------
    def step(p: Product) -> Step:
        return Step(product_id=p.id, name=p.name, brand=p.brand, type=p.type,
                    order=TYPE_ORDER[p.type])

    days: list[Day] = []
    for d, name in enumerate(DAYS):
        am, pm = [], []
        for p in basics:
            if "AM" in basic_slots[p.id]:
                am.append(step(p))
            if "PM" in basic_slots[p.id]:
                pm.append(step(p))
        for p in actives:
            if d in on[p.id]:
                (am if slot[p.id] == "AM" else pm).append(step(p))
        am.sort(key=lambda s: s.order)
        pm.sort(key=lambda s: s.order)
        days.append(Day(day=name, am=am, pm=pm))

    # ---- Step 7: warnings and the per-product summary --------------------
    shelf_families = set().union(*(catalog.families_of(p) for p in products)) if products else set()
    needs_spf = [catalog.timing[f] for f in shelf_families
                 if f in catalog.timing and catalog.timing[f].needs_sunscreen]
    if needs_spf and not any(p.type == "sunscreen" for p in products):
        warnings.append("Your shelf has a retinoid or AHA but no sunscreen. These make skin "
                        f"more sensitive to the sun, so add a sunscreen ({needs_spf[0].id}).")

    plan = []
    for p in products:
        if p.id in slot:
            item_slots, item_days = [slot[p.id]], [DAYS[d] for d in on[p.id]]
        else:
            item_slots, item_days = sorted(basic_slots[p.id]), (DAYS if basic_slots[p.id] else [])
        plan.append(PlanItem(product_id=p.id, name=f"{p.brand} {p.name}", slots=item_slots,
                             days=item_days, reasons=reasons[p.id] or ["Every day"]))

    return Routine(level=level, days=days, plan=plan, conflicts=conflicts, warnings=warnings)
