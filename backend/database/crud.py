from sqlalchemy.orm import Session
from databases import Database

from . import models, schemas


def get_item(db: Database, item_id: int):
    query = models.items.select().where(models.items.c.id == item_id)
    return db.fetch_one(query)


def get_items(db: Database, skip: int = 0, limit: int = 100):
    query = models.items.select(offset=skip, limit=limit)
    return db.fetch_all(query)


def create_item(db: Database, item: schemas.BaseItem):
    query = models.items.insert()
    return db.execute(query=query, values=item.dict())