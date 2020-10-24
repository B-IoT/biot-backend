from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from aiohttp import ClientSession
from typing import List
from databases import Database


import ujson

from database import crud, models, schemas
from database.db import database, engine
from kontakt import api
from settings import KEYS


models.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    return database


headers = {
    "Api-Key": KEYS["kontakt_api_key"],
    "Accept": "application/vnd.com.kontakt+json;version=10",
}
session = ClientSession(json_serialize=ujson.dumps, headers=headers)


@app.on_event("startup")
async def startup():
    await database.connect()
    is_initialized = await crud.is_initialized(database)
    items = await api.get_items(session)
    if is_initialized:
        await crud.update_items(database, items)
    else:
        await crud.add_items(database, items)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await database.disconnect()


@app.get("/items", response_model=List[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: Database = Depends(get_db)):
    items = await api.get_items(session)
    await crud.update_items(database, items)
    return await crud.get_items(db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, db: Database = Depends(get_db)):
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item = await api.get_item(session, db_item.kontaktId)
    await crud.update_item(database, item)

    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@app.post("/items", response_model=schemas.Item)
async def create_item(item: schemas.TypedItem, db: Database = Depends(get_db)):
    kontakt_item = await api.get_item(session, item.kontaktId)
    new_item = schemas.TypedItem(type=item.type, **kontakt_item.dict())
    last_record_id = await crud.add_item(db=db, item=new_item)

    return {**new_item.dict(), "id": last_record_id}