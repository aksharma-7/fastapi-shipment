from app.api.schemas.shipment import ShipmentUpdate, ShipmentCreate
from fastapi import APIRouter, HTTPException, status
from app.database.models import Shipment
from .dependencies import ServiceDep

router = APIRouter()


@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, service: ServiceDep):

    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )

    return shipment


@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    new_shipment = await service.add(shipment)

    return new_shipment


@router.patch("/shipment", response_model=Shipment)
async def update_shipment(
    id: int, shipment_update: ShipmentUpdate, service: ServiceDep
):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    shipment = await service.update(id, update)

    return shipment


@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)

    return {"detail": "Shipment deleted successfully"}
