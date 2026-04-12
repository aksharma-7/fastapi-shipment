from sqlmodel import Field
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel

class ShipmentStatus(Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"   # ✅ FIXED

    id: int | None = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime
