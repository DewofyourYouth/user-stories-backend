import datetime

from app.db import Product as ProductTable
from app.db import User
from fastapi import APIRouter, Query, status
from pydantic import BaseModel
from pytz import UTC

# from email import message
# from math import prod


router = APIRouter(prefix="/products", tags=["product"])


class PromptOption(BaseModel):
    key: int
    message: str
    action: str


class Prompt(BaseModel):
    system: bool
    message: str
    options: list[PromptOption]


class Product(BaseModel):
    product_id: int | None
    owner: str
    title: str
    persona: str | None
    created: datetime.time | None = datetime.datetime.now(tz=UTC)
    last_updated: datetime.time | None = datetime.datetime.now(tz=UTC)
    deleted: datetime.time | None


products = []


@router.get("/")
def list_all_products(user: str = Query()) -> list[Product]:
    user = User.select().where(User.username == user).get()
    return [Product(**p.__data__) for p in user.products if not p.deleted]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product)
def add_product(product: Product) -> Product:
    ProductTable.create(
        product_id=product.product_id,
        owner=product.owner,
        title=product.title,
        persona=product.persona,
        created=product.created,
        last_updated=product.last_updated,
        deleted=product.deleted,
    )
    return (
        ProductTable.select().where(ProductTable.title == product.title).get().__data__
    )


@router.get("/{id}/")
def get_product_by_id(id: int) -> Product:
    return ProductTable.get_by_id(id).__data__


@router.get("/{user}/")
def get_products_prompt(user: str) -> Prompt:
    user = User.select().where(User.username == user).get()
    options = [
        PromptOption(
            key=product.product_id, message=product.title, action="reviewProduct"
        )
        for product in user.products
    ]
    return Prompt(
        system=True,
        message=f"Great {user.first_name}! Which of your products would you like to review?",
        options=options,
    )
