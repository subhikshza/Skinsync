"""Loads the data files and finds conflicts between products.

Everything here is a pure function of the data: same shelf in, same conflicts out.
"""
import json
from itertools import combinations
from pathlib import Path

from .models import Conflict, ConflictRule, Ingredient, Product, Rules

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class Catalog:
    """All the read-only data, loaded once when the server starts."""

    def __init__(self, data_dir: Path = DATA_DIR):
        def load(name):
            return json.loads((data_dir / name).read_text(encoding="utf-8"))

        self.products = {p["id"]: Product(**p) for p in load("products.json")}
        self.ingredients = {i["id"]: Ingredient(**i) for i in load("ingredients.json")}
        self.rules = Rules(**load("rules.json"))

        # Fail early if a product lists an active we do not know.
        for p in self.products.values():
            for a in p.actives:
                if a not in self.ingredients:
                    raise ValueError(f"{p.id}: unknown ingredient '{a}'")

        # Look up a rule by its pair of families, in either order.
        self.rule_by_pair: dict[frozenset, ConflictRule] = {
            frozenset((r.family_a, r.family_b)): r for r in self.rules.conflicts
        }
        self.timing = {t.family: t for t in self.rules.timing}

        # "Strong" families are the ones a rule actually constrains.
        # Niacinamide is left out: its only rule is the myth note (R7).
        self.strong_families = set(self.timing)
        for r in self.rules.conflicts:
            if r.type != "myth":
                self.strong_families |= {r.family_a, r.family_b}

    def families_of(self, product: Product) -> set[str]:
        """Ingredient families in a product, e.g. {'retinoid'}."""
        fams = {self.ingredients[a].family for a in product.actives}
        fams.discard("none")
        return fams

    def is_active(self, product: Product) -> bool:
        """A leave-on product with at least one strong family.

        These are the products the scheduler has to place carefully.
        Cleansers are wash-off, so they are handled as basics.
        """
        return product.type != "cleanser" and bool(
            self.families_of(product) & self.strong_families
        )


def detect_conflicts(products: list[Product], catalog: Catalog) -> list[Conflict]:
    """Check every pair of products against the rules table."""
    found: list[Conflict] = []
    for p1, p2 in combinations(products, 2):          # every unordered pair
        seen_rules = set()
        for f1 in catalog.families_of(p1):
            for f2 in catalog.families_of(p2):
                rule = catalog.rule_by_pair.get(frozenset((f1, f2)))
                if rule is None or f1 == f2 or rule.id in seen_rules:
                    continue
                seen_rules.add(rule.id)

                # Relax the rule if one product is a face wash and the rule allows it.
                wash_off = rule.skip_if_wash_off and "cleanser" in (p1.type, p2.type)
                found.append(Conflict(
                    rule_id=rule.id,
                    product_a=p1.id, product_b=p2.id,
                    product_a_name=f"{p1.brand} {p1.name}",
                    product_b_name=f"{p2.brand} {p2.name}",
                    type=rule.type,
                    severity="info" if wash_off else rule.severity,
                    resolution="none" if wash_off else rule.resolution,
                    explanation=rule.explanation,
                    source_title=rule.source_title,
                    source_url=rule.source_url,
                    wash_off=wash_off,
                    resolved_how=(
                        "One of these is a face wash, so it is on the skin only briefly. "
                        "Allowed together." if wash_off
                        else "Not a real conflict. Allowed together." if rule.type == "myth"
                        else None
                    ),
                ))
    return found
