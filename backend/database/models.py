from sqlalchemy import Table, Column, Integer, Float, String, TIMESTAMP, Boolean

from .db import metadata

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("beaconId", String, index=True),
    Column("type", String, index=True),
    Column("service", String, index=True),
    Column("status", String, index=True),
    Column("battery", Integer),
    Column("lastSeen", TIMESTAMP, index=True),
    Column("latitude", Float, index=True),
    Column("longitude", Float, index=True),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, index=True),
    Column("disabled", Boolean),
    Column("hashedPassword", String),
)