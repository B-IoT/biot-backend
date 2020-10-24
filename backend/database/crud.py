from sqlalchemy.orm import Session
from databases import Database
from typing import List
import asyncio

from . import models, schemas


def is_initialized(db: Database) -> bool:
    query = models.items.select().limit(1)
    return db.fetch_one(query)


def get_item(db: Database, item_id: int) -> schemas.Item:
    query = models.items.select().where(models.items.c.id == item_id)
    return db.fetch_one(query)


def get_items(db: Database, skip: int = 0, limit: int = 100) -> List[schemas.Item]:
    query = models.items.select(offset=skip, limit=limit)
    return db.fetch_all(query)


def add_item(db: Database, item: schemas.BaseItem):  # for Kontakt
    query = models.items.insert()
    return db.execute(query=query, values=item.dict())


def add_item(db: Database, item: schemas.TypedItem):
    query = models.items.insert()
    return db.execute(query=query, values=item.dict())


def add_items(db: Database, items: List[schemas.BaseItem]):  # for Kontakt
    query = models.items.insert()
    return db.execute_many(query=query, values=[item.dict() for item in items])


def add_items(db: Database, items: List[schemas.TypedItem]):
    query = models.items.insert()
    return db.execute_many(query=query, values=[item.dict() for item in items])


def update_item(db: Database, item: schemas.BaseItem):
    query = models.items.update().where(models.items.c.kontaktId == item.kontaktId)
    return db.execute(query=query, values=item.dict())


def update_item(db: Database, item: schemas.TypedItem):  # for frontend
    query = models.items.update().where(models.items.c.kontaktId == item.kontaktId)
    return db.execute(query=query, values=item.dict())


def update_items(db: Database, items: List[schemas.BaseItem]):
    queries = []
    for item in items:
        query = models.items.update().where(models.items.c.kontaktId == item.kontaktId)
        queries.append(db.execute(query=query, values=item.dict()))

    return asyncio.gather(*queries)


def update_items(db: Database, items: List[schemas.TypedItem]):  # for frontend
    queries = []
    for item in items:
        query = models.items.update().where(models.items.c.kontaktId == item.kontaktId)
        queries.append(db.execute(query=query, values=item.dict()))

    return asyncio.gather(*queries)
