from sqlalchemy import Table, Column, Integer, Float, String

from .db import metadata

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("type", String, index=True),
    Column("status", String, index=True),
    Column("battery", Integer),
    Column("latitude", Float, index=True),
    Column("longitude", Float, index=True)
)