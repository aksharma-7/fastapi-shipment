from app.api.schemas.shipment import ShipmentUpdate
from datetime import timedelta
from datetime import datetime
from app.database.models import ShipmentStatus
from app.api.schemas.shipment import ShipmentCreate
from fastapi import APIRouter, HTTPException, status
from app.database.session import SessionDep
from app.database.models import Shipment

router = APIRouter()


@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):

    shipment = await session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )

    return shipment


@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )

    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    return {"id": new_shipment.id}


@router.patch("/shipment", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    shipment = await session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)

    return shipment


@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    shipment = await session.get(Shipment, id)

    await session.delete(shipment)
    await session.commit()

    return {"detail": "Shipment deleted successfully"}
