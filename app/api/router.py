from app.services.shipment import ShipmentService
from app.api.schemas.shipment import ShipmentUpdate, ShipmentCreate
from fastapi import APIRouter, HTTPException, status
from app.database.session import SessionDep
from app.database.models import Shipment

router = APIRouter()


@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):

    shipment = ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )

    return shipment


@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> Shipment:
    new_shipment = await ShipmentService(session).add(shipment)

    return new_shipment


@router.patch("/shipment", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    shipment = ShipmentService(session).update(shipment_update)

    return shipment

 
@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    await ShipmentService(session).delete(id)

    return {"detail": "Shipment deleted successfully"}
