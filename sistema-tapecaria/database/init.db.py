import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, "../database/database.db")
schema_path = os.path.join(BASE_DIR, "../database/schema.sql")

connection = sqlite3.connect(db_path)

with open(schema_path, 'r', encoding='utf-8') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Banco de dados criado com sucesso!")