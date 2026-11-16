"""Data shapes used across the app.

Pydantic checks every JSON file and every API request against these models,
so a typo in a data file fails at startup instead of in front of a user.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field

Family = Literal[
    "retinoid", "aha", "bha", "vitamin_c", "benzoyl_peroxide", "niacinamide", "none"
]
ProductType = Literal["cleanser", "toner", "serum", "treatment", "moisturizer", "sunscreen"]
Slot = Literal["AM", "PM"]
Level = Literal["beginner", "regular"]


# ---------- data files ----------

class Ingredient(BaseModel):
    id: str
    name: str
    family: Family
    aliases: list[str] = []


class Product(BaseModel):
    id: str
    name: str
    brand: str
    brand_origin: str
    type: ProductType
    price_inr: int
    actives: list[str]          # ingredient ids
    source_url: str
    note: Optional[str] = None


class ConflictRule(BaseModel):
    id: str
    family_a: Family
    family_b: Family
    type: Literal["irritation", "deactivation", "myth"]
    severity: Literal["high", "medium", "info"]
    resolution: Literal["separate_days", "separate_slots", "none"]
    skip_if_wash_off: bool
    explanation: str
    source_title: str
    source_url: str


class TimingRule(BaseModel):
    id: str
    family: Family
    allowed_slots: list[Slot]
    max_days_per_week: dict[Level, int]
    no_consecutive_days: dict[Level, bool]
    needs_sunscreen: bool
    explanation: str
    source_title: str
    source_url: str


class Rules(BaseModel):
    conflicts: list[ConflictRule]
    timing: list[TimingRule]


# ---------- API requests ----------

class ShelfRequest(BaseModel):
    product_ids: list[str] = Field(min_length=1, max_length=15)


class RoutineRequest(ShelfRequest):
    level: Level = "beginner"


# ---------- API responses ----------

class Conflict(BaseModel):
    rule_id: str
    product_a: str               # product id
    product_b: str
    product_a_name: str
    product_b_name: str
    type: str
    severity: str                # may be downgraded to "info" for a face wash
    resolution: str
    explanation: str
    source_title: str
    source_url: str
    wash_off: bool = False       # True when the rule was relaxed for a cleanser
    resolved_how: Optional[str] = None   # filled in by the scheduler


class Step(BaseModel):
    product_id: str
    name: str
    brand: str
    type: ProductType
    order: int


class Day(BaseModel):
    day: str
    am: list[Step]
    pm: list[Step]


class PlanItem(BaseModel):
    """One line per product: when it is used and why."""
    product_id: str
    name: str
    slots: list[Slot]
    days: list[str]
    reasons: list[str]


class Routine(BaseModel):
    level: Level
    days: list[Day]
    plan: list[PlanItem]
    conflicts: list[Conflict]
    warnings: list[str]
