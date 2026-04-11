import sqlite3


connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER,
        content TEXT,
        weight REAL,
        status TEXT
    )
""")

# cursor.execute("""
#     INSERT INTO shipment
#     VALUES
#         (12701, "glassware", 5.6, "placed"),
#         (12702, "electronics", 1.5, "in_transit"),
#         (12703, "furniture", 24.5, "delivered"),
#         (12704, "documents", 1.2, "placed"),
#         (12705, "kitchenware", 12.8, "in_transit"),
#         (12706, "clothing", 2.2, "out_for_delivery"),
#         (12707, "books", 3.5, "delivered")
# """)

cursor.execute("""
    SELECT *
    FROM shipment
    WHERE id = 12701
""")

print(cursor.fetchone())


connection.commit()
connection.close()