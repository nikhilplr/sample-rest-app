from fastapi import FastAPI
from pydantic import BaseModel

#
# This is a simple application that stores data on post calls and send the data on get request
#

app = FastAPI()

# Initial data storage
data = {"message": "A python based rest API"}

# GET request to fetch data
@app.get("/data")
def get_data():
    return data

@app.get("/health")
def get_data():
    return {"health": "Up Running"}

# Data model for POST request
class Item(BaseModel):
    name: str
    value: int

# POST request to add data
@app.post("/data")
def post_data(item: Item):
    data.update({"name": item.name, "value": item.value})
    return {"status": "Data updated successfully", "data": data}
 