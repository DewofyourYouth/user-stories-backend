import datetime

from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
)

db = PostgresqlDatabase(
    "user_stories",
    user="jacobshore",
    password="chani",
    host="localhost",
    port=5432,
)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db
        autorollback = True


class Organization(BaseModel):
    org_id = AutoField()
    org_name = CharField(max_length=50, null=False)


class User(BaseModel):
    username = CharField(primary_key=True, max_length=10)
    title = CharField(max_length=50, null=False)
    first_name = CharField(max_length=30, null=False)
    last_name = CharField(max_length=30, null=False)
    organization = ForeignKeyField(Organization, backref="members")


class Product(BaseModel):
    product_id = AutoField()
    title = CharField(max_length=100, null=False, unique=True)
    persona = CharField(max_length=100)
    created = DateTimeField(default=datetime.datetime.now)
    last_updated = DateTimeField(default=datetime.datetime.now)
    deleted = DateTimeField(default=None)
    owner = ForeignKeyField(User, backref="products")


class UserStory(BaseModel):
    us_id = AutoField()
    product = ForeignKeyField(Product, backref="user_stories")
    goal = CharField(max_length=100)
    person = CharField(max_length=30)
