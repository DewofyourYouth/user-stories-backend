from fastapi import APIRouter, Query, status
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["product"])


class Product(BaseModel):
    owner: str
    title: str


products = []


@router.get("/", response_model=list[Product])
def list_all_products(user: str = Query()) -> list[Product]:
    return [product for product in products if product.owner == user]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product)
def add_product(product: Product) -> Product:
    products.append(product)
    return product
