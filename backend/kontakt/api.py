import aiohttp
from database import schemas
from typing import List

API_URL = "https://api.kontakt.io"


# Get all items
async def get_items(session: aiohttp.ClientSession) -> List[schemas.BaseItem]:
    async with session.get(f"{API_URL}/device") as r:
        # TODO: extract relevant attributes
        json = await r.json()
        devices = json["devices"]

        return await r.json()

async def get_item(session: aiohttp.ClientSession, item_id: int) -> schemas.BaseItem:
    async with session.get(f"{API_URL}/device", params={"uniqueId": [item_id]}) as r:
        # TODO: extract relevant attributes
        json = await r.json()
        devices = json["devices"]

        return await r.json()
