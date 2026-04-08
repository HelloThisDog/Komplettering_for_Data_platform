from typing import Union
from fastapi import FastAPI

app = FastAPI(title="top 5 API")

@app.get("/")
def root():
    return {"Hello": "world"}