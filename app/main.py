from app.database.session import create_db_tables
from contextlib import asynccontextmanager
from .database import Database
from fastapi import FastAPI, status, HTTPException
from typing import Any
from scalar_fastapi import get_scalar_api_reference
from rich import print, panel

from .schemas import ShipmentStatus, ShipmentRead, ShipmentCreate, ShipmentUpdate

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)


db = Database()

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int | None = None):

    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )

    return shipment


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)

    return {"id": new_id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    shipment = db.update(id, body)

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"message": "Shipment deleted successfully"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
