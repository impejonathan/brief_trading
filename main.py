from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    liste = [i for i in range(100) if i%5==0]
    return{"la liste": liste}


# conn = sqlite3.connect("db_trading.db")

# class Item(BaseModel):
#     name: str
#     price: float

# @app.post("/items/")
# async def create_item(item: Item):
#     cur = conn.cursor()
#     cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
#     conn.commit()
#     return {"item": item}

# @app.get("/items/")
# async def read_items():
#     cur = conn.cursor()
#     cur.execute("SELECT name, price FROM items")
#     items = cur.fetchall()
#     return {"items": items}