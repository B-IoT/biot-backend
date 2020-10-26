import aiohttp
from database import schemas
from typing import List
from datetime import datetime
from collections import defaultdict

API_URL = "https://api.kontakt.io"


def extract_item_from_json(device_json, status_json):
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


# async def trigger_devices_update(session: aiohttp.ClientSession, beacon_ids: List[str]):
#     async with session.post(
#         f"{API_URL}/device/update",
#         data={"uniqueId": beacon_ids, "deviceType": "BEACON"},
#         headers={
#             "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
#             "Api-Key": KEYS["kontakt_api_key"],
#             "Accept": "application/vnd.com.kontakt+json;version=10",
#         },
#     ) as r:
#         print(await r.text())


# Get all items
async def get_items(session: aiohttp.ClientSession) -> List[schemas.BaseItem]:
    async with session.get(f"{API_URL}/device", params={"deviceType": "BEACON"}) as r1:
        async with session.get(f"{API_URL}/device/status") as r2:
            json = await r1.json()
            status_json = await r2.json()
            devices_json = json["devices"]
            statuses_json = status_json["statuses"]

            devices_statuses = combine_devices_statuses(devices_json, statuses_json)

            devices = [
                extract_item_from_json(device_status[0], device_status[1])
                for device_status in devices_statuses
            ]

            return devices


async def get_item(session: aiohttp.ClientSession, beacon_id: int) -> schemas.BaseItem:
    async with session.get(f"{API_URL}/device", params={"uniqueId": [beacon_id]}) as r1:
        async with session.get(
            f"{API_URL}/device/status", params={"uniqueId": [beacon_id]}
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
