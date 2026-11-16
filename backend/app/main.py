"""FastAPI app: thin routes that validate input and call the engine."""
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .engine import Catalog, detect_conflicts
from .models import Conflict, Product, RoutineRequest, Routine, Rules, ShelfRequest
from .scheduler import build_week

app = FastAPI(title="SkinSync API", version="1.0.0",
              description="Conflict checker and weekly routine builder. Not medical advice.")

# The React app runs on a different address, so the browser needs CORS allowed.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])

catalog = Catalog()          # data files are read once, at startup


def pick(product_ids: list[str]) -> list[Product]:
    """Turn ids into products. Unknown id -> 404 naming the bad id."""
    unique = list(dict.fromkeys(product_ids))          # drop duplicates, keep order
    missing = [i for i in unique if i not in catalog.products]
    if missing:
        raise HTTPException(status_code=404, detail=f"Unknown product id(s): {missing}")
    return [catalog.products[i] for i in unique]


@app.get("/api/health")
def health():
    return {"status": "ok", "products": len(catalog.products)}


@app.get("/api/products", response_model=list[Product])
def list_products(q: Optional[str] = None, brand: Optional[str] = None,
                  type: Optional[str] = None):
    items = list(catalog.products.values())
    if q:
        items = [p for p in items if q.lower() in f"{p.brand} {p.name}".lower()]
    if brand:
        items = [p for p in items if p.brand.lower() == brand.lower()]
    if type:
        items = [p for p in items if p.type == type]
    return items


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = pick([product_id])[0]
    return {**product.model_dump(), "families": sorted(catalog.families_of(product))}


@app.get("/api/ingredients")
def list_ingredients():
    return list(catalog.ingredients.values())


@app.get("/api/rules", response_model=Rules)
def get_rules():
    return catalog.rules


@app.post("/api/conflicts/check", response_model=list[Conflict])
def check_conflicts(body: ShelfRequest):
    return detect_conflicts(pick(body.product_ids), catalog)


@app.post("/api/routines/generate", response_model=Routine)
def generate_routine(body: RoutineRequest):
    return build_week(pick(body.product_ids), body.level, catalog)
