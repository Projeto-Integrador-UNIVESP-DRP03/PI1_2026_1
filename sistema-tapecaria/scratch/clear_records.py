import sqlite3
import os

db_path = os.path.join("instance", "database.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables_to_clear = [
        "pedidos",
        "orcamento_tecido",
        "orcamento_costura",
        "orcamento_cor",
        "orcamento_espuma",
        "orcamento"
    ]
    
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Tabela {table} limpa com sucesso.")
        except sqlite3.OperationalError as e:
            print(f"Erro ao limpar tabela {table}: {e}")
                
    conn.commit()
    conn.close()
    print("Limpeza concluída.")
else:
    print(f"Banco de dados não encontrado em {db_path}")
