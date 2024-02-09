"""
This is a simple FastAPI project for learning purposes
"""

from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    A class to represent an item in the inventory
    """
    name: str
    details: Optional[str] = None
    price: float


class UpdateItem(BaseModel):
    """
    A class to update an item in the inventory
    """
    name: Optional[str] = None
    details: Optional[str] = None
    price: Optional[float] = None


inventory = {}


@app.get("/get-item/{item_id}")
def get_item_by_id(item_id: int = Path(description="The ID of the item being searched", gt=0)):
    """
    Get an item on the inventory by its ID.
    Should not work if ID does not exist.
    """
    if item_id in inventory:
        return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/get-by-name")
def get_item_by_name(name: str = Query(None, title="Name", \
    description="Name of the item being searched")):
    """
    Get an item on the inventory by its name.
    Should not work if ID or name does not exist.
    """
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    """
    Create an item in the inventory.
    Should not work if ID already exists.
    """
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    """
    Update an item in the inventory.
    Should not work if ID does not exist.
    """
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if item.name is not None:
        inventory[item_id].name = item.name
    if item.details is not None:
        inventory[item_id].details = item.details
    if item.price is not None:
        inventory[item_id].price = item.price
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item being searched")):
    """
    Remove an item from the inventory.
    Should not work if ID does not exist.
    """
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del inventory[item_id]
    return {"Success": f"Item with id={item_id} deleted"}
