from typing import Union

from fastapi import FastAPI
from Parser import Parser

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Success": "Ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/process")
def process():
    try:
        parser = Parser()
        parser.scrape()
    except Exception as e:
        print(e)
        print("Failed to scrape the catalogue.")
        return {"msg": "Failed"}
    return {"msg": "Success"}
