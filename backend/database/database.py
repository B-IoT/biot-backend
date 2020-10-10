from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./database/biot.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata = MetaData()

database = Database(DATABASE_URL)