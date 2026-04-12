from app.api.schemas.shipment import ShipmentUpdate
from datetime import timedelta
from datetime import datetime
from app.database.models import ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Shipment:
        return await self.session.get(Shipment, id)

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
        )

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(self, id: int, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)

        estimated_delivery = shipment_update.get("estimated_delivery")

        if estimated_delivery and estimated_delivery.tzinfo:
            shipment_update["estimated_delivery"] = estimated_delivery.replace(
                tzinfo=None
            )

        # Apply the dictionary updates to your SQLAlchemy model instance
        for key, value in shipment_update.items():
            setattr(shipment, key, value)

        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: int) -> None:
        shipment = await self.get(id)

        await self.session.delete(shipment)
        await self.session.commit()
