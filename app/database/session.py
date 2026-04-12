from sqlmodel import SQLModel
from sqlalchemy import create_engine

engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)