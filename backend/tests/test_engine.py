"""Tests for the two core functions. Run with: pytest (from the backend folder)."""
import pytest
from fastapi.testclient import TestClient

from app.engine import Catalog, detect_conflicts
from app.main import app
from app.scheduler import DAYS, build_week

catalog = Catalog()
client = TestClient(app)

RETINOL = "minimalist-retinol-03-serum"
GLYCOLIC = "minimalist-glycolic-acid-8-toner"
VITC = "minimalist-vitamin-c-10-serum"
NIACINAMIDE = "minimalist-niacinamide-10-serum"
SAL_SERUM = "minimalist-salicylic-acid-2-serum"
SAL_WASH = "minimalist-salicylic-lha-2-cleanser"
BP_WASH = "dermaco-benzoyl-peroxide-face-wash"
SUNSCREEN = "minimalist-spf-50-sunscreen"
MOISTURIZER = "minimalist-vitamin-b5-10-moisturizer"
GENTLE_WASH = "minimalist-b12-oat-gentle-cleanser"


def shelf(*ids):
    return [catalog.products[i] for i in ids]


def days_with(routine, product_id, slot):
    return [d.day for d in routine.days
            if any(s.product_id == product_id for s in getattr(d, slot))]


# ---------- data ----------

def test_catalog_size_and_sources():
    assert 25 <= len(catalog.products) <= 30
    assert all(p.source_url.startswith("https://") for p in catalog.products.values())
    assert all(r.source_url.startswith("https://") for r in catalog.rules.conflicts)


# ---------- detect_conflicts ----------

def test_retinol_and_glycolic_conflict():
    found = detect_conflicts(shelf(RETINOL, GLYCOLIC), catalog)
    assert [c.rule_id for c in found] == ["R1"]
    assert found[0].severity == "high"


def test_niacinamide_and_vitamin_c_is_only_a_myth_note():
    found = detect_conflicts(shelf(NIACINAMIDE, VITC), catalog)
    assert [c.type for c in found] == ["myth"]
    assert found[0].severity == "info"


def test_salicylic_face_wash_is_relaxed_but_serum_is_not():
    wash = detect_conflicts(shelf(RETINOL, SAL_WASH), catalog)[0]
    serum = detect_conflicts(shelf(RETINOL, SAL_SERUM), catalog)[0]
    assert wash.wash_off and wash.severity == "info"
    assert not serum.wash_off and serum.severity == "medium"


def test_no_conflict_between_basics():
    assert detect_conflicts(shelf(GENTLE_WASH, MOISTURIZER, SUNSCREEN), catalog) == []


# ---------- build_week ----------

@pytest.mark.parametrize("level", ["beginner", "regular"])
def test_retinol_and_glycolic_never_share_a_night(level):
    r = build_week(shelf(RETINOL, GLYCOLIC, MOISTURIZER, SUNSCREEN), level, catalog)
    assert not set(days_with(r, RETINOL, "pm")) & set(days_with(r, GLYCOLIC, "pm"))


def test_retinol_is_never_in_the_morning():
    r = build_week(shelf(RETINOL, VITC, SUNSCREEN), "regular", catalog)
    assert days_with(r, RETINOL, "am") == []
    assert days_with(r, VITC, "pm") == []            # vitamin C stays in the AM
    assert days_with(r, VITC, "am") == DAYS          # and can be daily


def test_beginner_retinol_is_capped_and_not_two_nights_running():
    r = build_week(shelf(RETINOL, MOISTURIZER, SUNSCREEN), "beginner", catalog)
    nights = [DAYS.index(d) for d in days_with(r, RETINOL, "pm")]
    assert len(nights) == 3
    assert all((n + 1) % 7 not in nights for n in nights)      # also checks Sun -> Mon


def test_regular_retinol_can_be_nightly():
    r = build_week(shelf(RETINOL, SUNSCREEN), "regular", catalog)
    assert len(days_with(r, RETINOL, "pm")) == 7


def test_salicylic_serum_and_retinol_are_on_different_days():
    r = build_week(shelf(RETINOL, SAL_SERUM, SUNSCREEN), "beginner", catalog)
    sal_days = set(days_with(r, SAL_SERUM, "am")) | set(days_with(r, SAL_SERUM, "pm"))
    assert sal_days and not sal_days & set(days_with(r, RETINOL, "pm"))


def test_benzoyl_peroxide_wash_is_kept_away_from_retinol():
    r = build_week(shelf(RETINOL, BP_WASH, SUNSCREEN), "beginner", catalog)
    assert days_with(r, BP_WASH, "pm") == []
    assert days_with(r, BP_WASH, "am") == DAYS


def test_sunscreen_is_last_step_every_morning():
    r = build_week(shelf(GENTLE_WASH, VITC, MOISTURIZER, SUNSCREEN), "beginner", catalog)
    assert all(d.am[-1].type == "sunscreen" for d in r.days)
    assert all(d.am[0].type == "cleanser" for d in r.days)


def test_warning_when_no_sunscreen_with_retinol():
    r = build_week(shelf(RETINOL, MOISTURIZER), "beginner", catalog)
    assert any("sunscreen" in w for w in r.warnings)


def test_every_real_conflict_gets_a_resolution():
    r = build_week(shelf(RETINOL, GLYCOLIC, VITC, SAL_SERUM, BP_WASH, SUNSCREEN),
                   "beginner", catalog)
    assert all(c.resolved_how for c in r.conflicts)


def test_same_input_gives_same_output():
    ids = shelf(RETINOL, GLYCOLIC, VITC, SUNSCREEN)
    assert build_week(ids, "beginner", catalog) == build_week(ids, "beginner", catalog)


# ---------- API ----------

def test_api_generate_and_errors():
    ok = client.post("/api/routines/generate",
                     json={"product_ids": [RETINOL, GLYCOLIC, SUNSCREEN], "level": "beginner"})
    assert ok.status_code == 200 and len(ok.json()["days"]) == 7
    assert client.post("/api/routines/generate", json={"product_ids": ["nope"]}).status_code == 404
    assert client.post("/api/routines/generate", json={"product_ids": []}).status_code == 422
    assert client.get("/api/products", params={"brand": "Minimalist"}).json()
    assert len(client.get("/api/rules").json()["conflicts"]) == 7


def test_face_wash_that_clashes_in_both_routines_is_left_out_with_a_warning():
    # Benzoyl peroxide wash clashes with vitamin C (AM) and retinol (PM).
    r = build_week(shelf(RETINOL, VITC, BP_WASH, SUNSCREEN), "beginner", catalog)
    assert days_with(r, BP_WASH, "am") == [] and days_with(r, BP_WASH, "pm") == []
    assert any("Benzoyl Peroxide" in w for w in r.warnings)
    assert all("left out" in c.resolved_how for c in r.conflicts if BP_WASH in (c.product_a, c.product_b))
