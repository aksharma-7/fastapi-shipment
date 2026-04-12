from datetime import datetime
from pydantic import Field
from enum import Enum
from sqlmodel import SQLModel

class ShipmentStatus(Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel, table=True):
    __table__name = "shipment"
    
    id: int = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime
