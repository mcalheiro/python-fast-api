from typing import Optional
from fastapi import FastAPI
from fastapi import Path

app = FastAPI();

inventory = {
    1: {
        "name": "PSU",
        "details": "850W",
        "price": "200"
    }
}

@app.get("/")
def home():
    return {"Data": "Hello world"}

# http://127.0.0.1:8000/get-item/1
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the item being searched", gt=0)):
    return inventory[item_id]

# http://127.0.0.1:8000/get-by-name/?name=PSU
# http://127.0.0.1:8000/get-by-name/1/?name=PSU
@app.get("/get-by-name/{item_id}")
def get_item(item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}