from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path
import json
import os
from kafka import KafkaProducer
from contextlib import asynccontextmanager



if __name__ == "__main__":
    #reads data
    df = pd.DataFrame(pd.read_csv("gen1_pokemon_full.csv", sep=",")) #ngl I thought it was gonna be ";"" not "," caught me off guard for a min

    high_speed = df.sort_values(by="speed", ascending=False).iloc[:5, [0, 1, 8]] #limits the list down to the top 5 pokemon with highest speed
    high_speed.to_csv("top_5_speed.csv", index=False) #produces the csv

DATA_PATH = Path(__file__).parent/"top_5_speed.csv"

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
PRODUCTS_TOPIC = os.getenv("PRODUCTS_TOPIC", "products.created")



@asynccontextmanager    
async def lifespan(app: FastAPI):
    app.state.kafka_producer = KafkaProducer (
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,)

    yield

    try:
        app.state.kafka_producer.close()
    except Exception:
        pass


app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    df = pd.read_csv(DATA_PATH)
    return df.to_dict(orient="records")


@app.post("/products")
def post_product():
    df = pd.read_csv(DATA_PATH)

    events = []
    for _, row in df.iterrows():
        event = {
            "type": "product.created",
            "product_id": int(row["id"]),
            "name": row["name"],
            "speed": int(row["speed"]),
        }

        app.state.kafka_producer.send(
            PRODUCTS_TOPIC,
            key=str(row["id"]),
            value=event
        )

        events.append(event)

    app.state.kafka_producer.flush()

    return events
