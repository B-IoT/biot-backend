from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from databases import Database

from database import crud, schemas

SECRET_KEY = "74c7f92aad5815515b12925f120e6a20eeae42d4708424b7480fadd6a9e1f732"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

USERNAME = "6cc987f6a8433d8d335619c6400370ffaa2ce2bcd8e4a1dfa7a613ca112bd3d9"
PASSWORD = "9388e36e7fb01968c04c214d29884d475d7fc8ba9a609cc730606846e350f396"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(db: Database, email: str, password: str):
    user = schemas.UserInDB.parse_obj(await crud.get_user(db, email))
    if not user:
        return None
    if not verify_password(password, user.hashedPassword):
        return None

    return user
