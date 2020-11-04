from sqlalchemy import create_engine, MetaData
from databases import Database
from settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_size=3, max_overflow=0)

metadata = MetaData()

database = Database(DATABASE_URL)