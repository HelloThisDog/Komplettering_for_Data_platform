from typing import Union
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="top 5 API")

@app.get("/readfileplz/{top_5_speed.csv}")
def create_upload_file(file: UploadFile):
    return {"top five 5": "file.top_5_speed.csv"} 