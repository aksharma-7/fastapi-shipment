from contextlib import contextmanager
from typing import Any
from app.api.schemas.shipment import ShipmentCreate
from app.api.schemas.shipment import ShipmentUpdate
import sqlite3

class Database:
    def connect_to_db(self):
        print("connecting to the database")
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )""")
    
    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()
        
        new_id = result[0] + 1

        self.cur.execute("""
            INSERT INTO shipment
            VALUES
                (:id, :content, :weight, :status)
        """, {
            "id": new_id,
            **shipment.model_dump(),
            "status": "placed"
        })

        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT *
            FROM shipment
            WHERE id = ?
        """, (id,))

        row = self.cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        }

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cur.execute("""
            UPDATE shipment
            SET status = :status
            WHERE id = :id
        """, {
            "id": id,
            "status": shipment.status.value
        })

        self.conn.commit()

        return self.get(id)

    def delete(self, id: int) -> dict[str, str]:
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = ?
        """, (id,))

        self.conn.commit()

        return {"message": "Shipment deleted successfully"}

    def close(self):
        print("closing the connection")
        self.conn.close()

    # def __enter__(self):
    #     print("entered the context")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self

    # def __exit__(self, *args):
    #     print("exiting the context")
    #     self.close()


@contextmanager
def managed_db():
    db = Database()

    print("enter the setup")
    db.connect_to_db()
    db.create_table()

    yield db

    print("exiting the context")
    db.close()

with managed_db() as db:
    print(db.get(12701))

