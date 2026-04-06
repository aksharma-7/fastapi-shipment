from fastapi import FastAPI, status, HTTPException
from typing import Any
from scalar_fastapi import get_scalar_api_reference

from .schemas import Shipment, ShipmentStatus


app = FastAPI()


shipments = {
    12701: {
        "weight": 5.6,
        "content": "glassware",
        "destination": 110001,
        "status": ShipmentStatus.placed
    },
    12702: {
        "weight": 1.5,
        "content": "electronics",
        "destination": 400001,
        "status": ShipmentStatus.in_transit
    },
    12703: {
        "weight": 24.5,
        "content": "furniture",
        "destination": 600001,
        "status": ShipmentStatus.delivered
    },
    12704: {
        "weight": 1.2,
        "content": "documents",
        "destination": 700001,
        "status": ShipmentStatus.placed
    },
    12705: {
        "weight": 12.8,
        "content": "kitchenware",
        "destination": 500001,
        "status": ShipmentStatus.in_transit
    },
    12706: {
        "weight": 2.2,
        "content": "clothing",
        "destination": 560001,
        "status": ShipmentStatus.out_for_delivery
    },
    12707: {
        "weight": 3.5,
        "content": "books",
        "destination": 302001,
        "status": ShipmentStatus.delivered
    }
}

@app.get("/shipment", response_model=Shipment)
def get_shipment(id: int | None = None):

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, int]:

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": shipment.content,
        "weight": shipment.weight,
        "destination": shipment.destination,
        "status": ShipmentStatus.placed
    }

    return {"id": new_id}


@app.patch("/shipment")
def update_shipment(id: int, body: dict[str, ShipmentStatus]) -> dict[str, Any]:
    shipment = shipments[id]

    # if content:
    #     shipment["content"] = content
    # elif weight:
    #     shipment["weight"] = weight
    # elif status:
    #     shipment["status"] = status

    shipment.update(body)

    shipments[id] = shipment

    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)

    return {"message": "Shipment deleted successfully"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
