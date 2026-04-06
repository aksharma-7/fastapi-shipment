from pydantic import BaseModel, Field
from random import randint
from enum import Enum

def random_destination():
    return randint(10000, 99999)

class ShipmentStatus(Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(BaseModel):
    content: str = Field(description="Content of the shipment", max_length=30)
    weight: float = Field(description="Weight of the shipment in kg", le=25, ge=1)
    destination: int | None = Field(description="Destination zip code", default_factory=random_destination)
    status: ShipmentStatus = Field(description="Status of the shipment")