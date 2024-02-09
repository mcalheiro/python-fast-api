from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from constants import MINIMAL_INVENTORY

app = FastAPI();


class Item(BaseModel): 
    name: str
    details: Optional[str] = None
    price: float


class UpdateItem(BaseModel):
    name: Optional[str] = None
    details: Optional[str] = None
    price: Optional[float] = None

inventory = {}


@app.get("/")
def home():
    return {"Data": "Hello world"}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the item being searched", gt=0)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of the item being searched")):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"Data": "Not found"}


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists"}
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist"}
    if item.name != None:
        inventory[item_id].name = item.name
    if item.details != None:
        inventory[item_id].details = item.details
    if item.price != None:
        inventory[item_id].price = item.price
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item being searched")):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist"}
    del inventory[item_id]
    return {"Success": f"Item with id={item_id} deleted"}
