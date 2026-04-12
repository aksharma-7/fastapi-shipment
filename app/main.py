from datetime import timedelta
from datetime import datetime
from app.database.session import create_db_tables, SessionDep
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from app.database.models import Shipment

from .schemas import ShipmentStatus, ShipmentRead, ShipmentCreate, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):

    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )

    return shipment


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )

    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    shipment = session.get(Shipment, id)

    session.delete(shipment)
    session.commit()

    return {"detail": "Shipment deleted successfully"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
