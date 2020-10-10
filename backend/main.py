from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases import Database

from database import crud, models, schemas
from database.database import database, engine

models.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    return database


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/items", response_model=List[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: Database = Depends(get_db)):
    return await crud.get_items(db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, db: Database = Depends(get_db)):
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@app.post("/items", response_model=schemas.Item)
async def create_item(item: schemas.BaseItem, db: Database = Depends(get_db)):
    last_record_id = await crud.create_item(db=db, item=item)
    return {**item.dict(), "id": last_record_id}