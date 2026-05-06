import sqlite3
import os

db_path = os.path.join("instance", "database.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    columns = [
        ("banco_motorista", "BOOLEAN DEFAULT 0"),
        ("banco_passageiro", "BOOLEAN DEFAULT 0"),
        ("banco_traseiro", "BOOLEAN DEFAULT 0")
    ]
    
    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE orcamento ADD COLUMN {col_name} {col_type}")
            print(f"Coluna {col_name} adicionada com sucesso.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Coluna {col_name} já existe.")
            else:
                print(f"Erro ao adicionar {col_name}: {e}")
                
    conn.commit()
    conn.close()
else:
    print(f"Banco de dados não encontrado em {db_path}")
