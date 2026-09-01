import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


ASSOCIATION_TABLES = {
    "orcamento_tecido": ("id_orcamento_tecido", "id_orcamento", "id_tecido"),
    "orcamento_costura": ("id_orcamento_costura", "id_orcamento", "id_costura"),
    "orcamento_cor": ("id_orcamento_cor", "id_orcamento", "id_cor"),
}


def validate_table(connection, table_name, columns):
    primary_key, budget_id, catalog_id = columns
    null_count = connection.execute(
        f'SELECT COUNT(*) FROM "{table_name}" '
        f'WHERE "{budget_id}" IS NULL OR "{catalog_id}" IS NULL'
    ).fetchone()[0]
    if null_count:
        raise RuntimeError(
            f"{table_name} possui {null_count} registro(s) com relacionamento nulo. "
            "Corrija os dados antes da migração."
        )

    duplicate_count = connection.execute(
        f'SELECT COUNT(*) FROM '
        f'(SELECT "{budget_id}", "{catalog_id}" FROM "{table_name}" '
        f'GROUP BY "{budget_id}", "{catalog_id}" HAVING COUNT(*) > 1)'
    ).fetchone()[0]
    if duplicate_count:
        raise RuntimeError(
            f"{table_name} possui relacionamentos duplicados. "
            "Corrija os dados antes da migração."
        )


def rebuild_association_table(connection, table_name, columns):
    primary_key, budget_id, catalog_id = columns
    temporary_table = f"{table_name}__old"
    connection.execute(f'ALTER TABLE "{table_name}" RENAME TO "{temporary_table}"')
    connection.execute(
        f'''CREATE TABLE "{table_name}" (
            "{primary_key}" INTEGER NOT NULL PRIMARY KEY,
            "{budget_id}" INTEGER NOT NULL,
            "{catalog_id}" INTEGER NOT NULL,
            "obs_item" VARCHAR(200),
            FOREIGN KEY("{budget_id}") REFERENCES orcamento (id_orcamento),
            FOREIGN KEY("{catalog_id}") REFERENCES "{catalog_id.split("_")[1]}" ("{catalog_id}")
        )'''
    )
    connection.execute(
        f'INSERT INTO "{table_name}" '
        f'("{primary_key}", "{budget_id}", "{catalog_id}", obs_item) '
        f'SELECT "{primary_key}", "{budget_id}", "{catalog_id}", obs_item '
        f'FROM "{temporary_table}"'
    )
    connection.execute(f'DROP TABLE "{temporary_table}"')


def migrate_database(database_path):
    database_path = Path(database_path).resolve()
    if not database_path.exists():
        raise FileNotFoundError(f"Banco não encontrado: {database_path}")

    backup_path = database_path.with_name(
        f"{database_path.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{database_path.suffix}"
    )
    shutil.copy2(database_path, backup_path)

    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys=OFF")
        for table_name, columns in ASSOCIATION_TABLES.items():
            validate_table(connection, table_name, columns)

        duplicate_orders = connection.execute(
            "SELECT COUNT(*) FROM ("
            "SELECT id_orcamento FROM pedidos "
            "GROUP BY id_orcamento HAVING COUNT(*) > 1"
            ")"
        ).fetchone()[0]
        if duplicate_orders:
            raise RuntimeError(
                "pedidos possui mais de um pedido para o mesmo orçamento. "
                "Corrija os dados antes da migração."
            )

        with connection:
            for table_name, columns in ASSOCIATION_TABLES.items():
                rebuild_association_table(connection, table_name, columns)
            connection.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_pedido_orcamento "
                "ON pedidos (id_orcamento)"
            )
            connection.execute("PRAGMA foreign_keys=ON")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return backup_path


def main():
    parser = argparse.ArgumentParser(description="Aplica constraints de integridade ao SQLite.")
    parser.add_argument(
        "database",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1] / "instance" / "database.db"),
    )
    args = parser.parse_args()
    backup_path = migrate_database(args.database)
    print(f"Migração concluída. Backup criado em: {backup_path}")


if __name__ == "__main__":
    main()
