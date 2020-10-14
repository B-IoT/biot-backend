import aiohttp

API_URL = "https://api.kontakt.io"


async def get_items(session: aiohttp.ClientSession):
    async with session.get(f"{API_URL}/device") as r:
        # TODO: extract relevant attributes
        return await r.json()
