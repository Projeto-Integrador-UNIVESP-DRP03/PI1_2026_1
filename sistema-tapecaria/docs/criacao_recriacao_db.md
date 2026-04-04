# Criação e Recriação do Banco de Dados

Este documento descreve **como criar, recriar e atualizar o banco de dados da aplicação** utilizando Flask e SQLAlchemy.

---

# 1. Pré-requisitos

Antes de criar o banco de dados, verifique se:

* O ambiente virtual está ativado
* As dependências estão instaladas
* A estrutura do projeto está correta

Estrutura esperada do projeto:

```
sistema-tapecaria
│
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│
├── database
│   └── init_db.py
│
├── instance
│   └── database.db
│
├── app.py
├── requirements.txt
```

O banco SQLite será criado em:

```
instance/database.db
```

---

# 2. Estrutura do Banco

O banco é criado automaticamente a partir das classes definidas no arquivo:

```
app/models.py
```

Cada classe representa uma **tabela do banco de dados**.

Exemplo:

```python
class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
```

Quando o banco é criado, o SQLAlchemy gera automaticamente as tabelas com base nesses modelos.

---

# 3. Script de criação do banco

O projeto possui um script responsável por criar o banco:

```
database/init_db.py
```

Conteúdo do arquivo:

```python
from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

print("Banco recriado com sucesso!")
```

Esse script:

1. cria a aplicação Flask
2. conecta ao banco SQLite
3. apaga todas as tabelas existentes
4. recria as tabelas com base nos models

---

# 4. Como criar o banco pela primeira vez

No terminal, dentro da pasta do projeto:

```
sistema-tapecaria
```

execute:

```
python database/init_db.py
```

Se tudo estiver correto, aparecerá:

```
Banco recriado com sucesso!
```

E o arquivo será criado em:

```
instance/database.db
```

---

# 5. Quando recriar o banco

O banco precisa ser recriado sempre que houver mudanças estruturais nos models, por exemplo:

* adicionar uma tabela
* remover uma tabela
* adicionar uma coluna
* alterar tipo de coluna
* alterar chave estrangeira

Após modificar `models.py`, execute novamente:

```
python database/init_db.py
```

---

# 6. Atenção ao usar drop_all()

O comando:

```
db.drop_all()
```

remove **todas as tabelas do banco de dados**.

Isso significa que **todos os dados serão apagados**.

Esse procedimento deve ser usado **apenas durante o desenvolvimento**.

---

# 7. Executar a aplicação

Depois que o banco for criado, a aplicação pode ser iniciada normalmente:

```
python app.py
```

A aplicação Flask iniciará utilizando o banco localizado em:

```
instance/database.db
```

---

# 8. Fluxo recomendado de desenvolvimento

Sempre que alterar o modelo de dados:

1. editar `app/models.py`
2. recriar o banco:

```
python database/init_db.py
```

3. iniciar a aplicação:

```
python app.py
```

---

# 9. Observação

Este projeto utiliza:

* Flask
* SQLAlchemy
* SQLite

O SQLAlchemy é responsável por mapear **classes Python em tabelas do banco de dados** (ORM – Object Relational Mapping).
