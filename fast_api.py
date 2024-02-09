from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from constants import MINIMAL_INVENTORY

app = FastAPI();

class Item(BaseModel): 
    name: str
    details: Optional[str] = None
    price: float

inventory = MINIMAL_INVENTORY

@app.get("/")
def home():
    return {"Data": "Hello world"}

# http://127.0.0.1:8000/get-item/1
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the item being searched", gt=0)):
    return inventory[item_id]

# http://127.0.0.1:8000/get-by-name/?name=PSU
# http://127.0.0.1:8000/get-by-name/1/?name=PSU
@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of the item being searched")):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists"}
    inventory[item_id] = {
        "name": item.name,
        "details": item.details,
        "price": item.price
    }
    return inventory[item_id]