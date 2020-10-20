from sqlalchemy.orm import Session
from databases import Database
from typing import List

from . import models, schemas

def is_initialized(db: Database) -> bool:
    query = models.items.select().limit(1)
    return db.fetch_one(query)

def get_item(db: Database, item_id: int) -> schemas.BaseItem:
    query = models.items.select().where(models.items.c.id == item_id)
    return db.fetch_one(query)


def get_items(db: Database, skip: int = 0, limit: int = 100) -> List[schemas.BaseItem]:
    query = models.items.select(offset=skip, limit=limit)
    return db.fetch_all(query)


def add_item(db: Database, item: schemas.BaseItem):
    query = models.items.insert()
    return db.execute(query=query, values=item.dict())


def add_items(db: Database, items: List[schemas.BaseItem]):
    query = models.items.insert()
    return db.execute_many(query=query, values=[item.dict() for item in items])


def update_item(db: Database, item: schemas.BaseItem):
    query = models.items.update()
    return db.execute(query=query, values=item.dict())


def update_items(db: Database, items: List[schemas.BaseItem]):
    query = models.items.update()
    return db.execute_many(query=query, values=[item.dict() for item in items])