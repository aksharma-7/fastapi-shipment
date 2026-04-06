from fastapi import FastAPI, status, HTTPException
from typing import Any
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed"
    },
    12702: {
        "weight": 1.5,
        "content": "electronics",
        "status": "shipped"
    },
    12703: {
        "weight": 45.0,
        "content": "furniture",
        "status": "delivered"
    },
    12704: {
        "weight": 0.2,
        "content": "documents",
        "status": "processing"
    },
    12705: {
        "weight": 12.8,
        "content": "kitchenware",
        "status": "in transit"
    },
    12706: {
        "weight": 2.2,
        "content": "clothing",
        "status": "packed"
    },
    12707: {
        "weight": 0.5,
        "content": "books",
        "status": "cancelled"
    }
}

@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:

    if id not in shipments:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, int]:
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Shipment weight cannot be greater than 25kg"
        )
    
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed"
    }

    return {"id": new_id}

@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {
        field: shipments[id][field]
    }

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
