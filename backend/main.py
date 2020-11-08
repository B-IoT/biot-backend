from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials,
)
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from aiohttp import ClientSession
from typing import List, Any
from databases import Database
from jose import jwt, JWTError

import ujson
import secrets
import os


from database import crud, models, schemas
from database.db import database, engine
from api import api
from security import security
from settings import KONTAKT_API_KEY


models.metadata.create_all(bind=engine)

app = FastAPI()

user_creation_security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost",
    "http://localhost:3000",  # TODO: add frontend url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
def get_db():
    return database


async def get_current_user(
    db: Database = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = security.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = schemas.User.parse_obj(await crud.get_user(db, email=token_data.email))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


headers = {
    "Api-Key": KONTAKT_API_KEY,
}
session = ClientSession(json_serialize=ujson.dumps, headers=headers)


@app.on_event("startup")
async def startup():
    await database.connect()
    # is_initialized = await crud.is_initialized(database)
    # items = await api.get_items(session)
    # # await api.trigger_devices_update(session, [item.beaconId for item in items])
    # # items = await api.get_items(session)
    # if is_initialized:
    #     await crud.update_items(database, items)
    # else:
    #     await crud.add_items(database, items)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await database.disconnect()


@app.post("/token", response_model=security.Token)
async def login_for_access_token(
    db: Database = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/items", response_model=List[schemas.Item])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Database = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    # items = await api.get_items(session)
    # # await api.trigger_devices_update(session, [item.beaconId for item in items])
    # # items = await api.get_items(session)
    # await crud.update_items(database, items)
    items = await crud.get_items(db, skip=skip, limit=limit)
    return [schemas.Item.parse_obj(item) for item in items]


@app.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(
    item_id: int,
    db: Database = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    # db_item = await crud.get_item(db, item_id=item_id)
    # if db_item is None:
    #     raise HTTPException(status_code=404, detail="Item not found")

    # # item = await api.get_item(session, db_item.beaconId)
    # # await api.trigger_devices_update(session, [item.beaconId])
    # item = await api.get_item(session, db_item.beaconId)
    # await crud.update_item(database, item)

    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return schemas.Item.parse_obj(db_item)


@app.post("/items", response_model=schemas.Item)
async def create_item(
    item: schemas.TypedItem,
    db: Database = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    # beacon_item = await api.get_item(session, item.beaconId)
    # # await api.trigger_devices_update(session, [beacon_item.beaconId])
    # # beacon_item = await api.get_item(session, item.beaconId)

    # new_item = schemas.TypedItem(
    #     type=item.type, service=item.service, **beacon_item.dict()
    # )
    last_record_id = await crud.add_item(db=db, item=item)

    return {**item.dict(), "id": last_record_id}


def authenticate_for_user_creation(
    credentials: HTTPBasicCredentials = Depends(user_creation_security),
):
    correct_username = secrets.compare_digest(credentials.username, security.USERNAME)
    correct_password = secrets.compare_digest(credentials.password, security.PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/users/create", response_model=schemas.User)
async def create_user(
    user: schemas.UserToCreate,
    db: Database = Depends(get_db),
    username: str = Depends(authenticate_for_user_creation),
):
    last_record_id = await crud.create_user(db=db, user=user)
    return {**user.dict(), "id": last_record_id}


@app.post("/echo")
async def echo(data: Any = Body(...)):
    return data