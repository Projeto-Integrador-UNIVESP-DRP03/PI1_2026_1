import sqlite3 # Importa a biblioteca para trabalhar com SQLite no python

connection = sqlite3.connect("../database/database.db") # onde será armazenado o banco de dados, caso não exista ele será criado
with open('../database/schema.sql', 'r',encoding='utf-8') as f:
    connection.executescript(f.read()) # executa o script SQL contido no arquivo schema.sql para criar as tabelas e estruturas necessárias no banco de dados

connection.commit()
connection.close()