import aiohttp
from database import schemas
from typing import List
from datetime import datetime
from collections import defaultdict

API_URL = "https://api.kontakt.io"
APPS_API_URL = "https://apps-api.prod.kontakt.io/v2"

COMMON_HEADERS = {"Accept": "application/vnd.com.kontakt+json;version=10"}


def extract_item_from_json(device_json, status_json, positions):
    # TODO: compute status
    return schemas.BaseItem(
        beaconId=device_json["uniqueId"],
        battery=status_json["batteryLevel"],
        lastSeen=datetime.fromtimestamp(device_json["lastSeen"]),
        latitude=device_json["lat"],
        longitude=device_json["lng"],
    )


def combine_devices_statuses(devices_json, statuses_json):
    devices_statuses = defaultdict(list)
    for d in devices_json:
        devices_statuses[d["uniqueId"]].append(d)

    for s in statuses_json:
        devices_statuses[s["uniqueId"]].append(s)

    return devices_statuses.values()


async def get_positions(session: aiohttp.ClientSession):
    async with session.get(
        f"{APPS_API_URL}/positions",
    ) as r:
        json = await r.json()
        content = json["content"]
        return [(device["lat"], device["lng"], device["trackingId"]) for device in content]


# Get all items
async def get_items(session: aiohttp.ClientSession) -> List[schemas.BaseItem]:
    async with session.get(
        f"{API_URL}/device", headers=COMMON_HEADERS, params={"deviceType": "BEACON"}
    ) as r1:
        async with session.get(
            f"{API_URL}/device/status", headers=COMMON_HEADERS
        ) as r2:
            json = await r1.json()
            status_json = await r2.json()
            devices_json = json["devices"]
            statuses_json = status_json["statuses"]

            devices_statuses = combine_devices_statuses(devices_json, statuses_json)
            positions = await get_positions(session)

            devices = [
                extract_item_from_json(device_status[0], device_status[1], positions)
                for device_status in devices_statuses
            ]

            
            return devices


async def get_item(session: aiohttp.ClientSession, beacon_id: int) -> schemas.BaseItem:
    async with session.get(
        f"{API_URL}/device", headers=COMMON_HEADERS, params={"uniqueId": [beacon_id]}
    ) as r1:
        async with session.get(
            f"{API_URL}/device/status",
            headers=COMMON_HEADERS,
            params={"uniqueId": [beacon_id]},
        ) as r2:
            json = await r1.json()
            status_json = await r2.json()
            devices_json = json["devices"]
            statuses_json = status_json["statuses"]

            devices_statuses = combine_devices_statuses(devices_json, statuses_json)

            device = [
                extract_item_from_json(device_status[0], device_status[1])
                for device_status in devices_statuses
            ][0]

            return device
