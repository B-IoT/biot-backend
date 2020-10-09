from typing import Optional

from fastapi import FastAPI, WebSocket

# TODO database

app = FastAPI()

@app.get("/items")
async def get_items():
    # TODO
    pass

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # TODO
    pass


@app.get("/")
async def read_root():
    return {"Hello": "World"}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")