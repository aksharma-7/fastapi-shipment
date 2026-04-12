from datetime import datetime
from app.database.models import ShipmentStatus
from pydantic import BaseModel, Field
from random import randint

def random_destination():
    return randint(10000, 99999)

# class ShipmentRead(BaseModel):
#     content: str = Field(description="Content of the shipment", max_length=30)
#     weight: float = Field(description="Weight of the shipment in kg", le=25, ge=1)
#     destination: int | None = Field(description="Destination zip code", default_factory=random_destination)
#     status: ShipmentStatus = Field(description="Status of the shipment")

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
