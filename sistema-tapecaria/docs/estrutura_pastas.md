# Estrutura de pastas do Sistema
```
sistema-tapecaria
│
├── app
│   ├── __init__.py
│   ├── models.py       [classes das tabelas usadas]
│   └── routes.py       [rota das páginas da aplicação]
│
├── database
│   ├── schema.sql                  Criação das tabelas
|   ├── init.db.py                  Inicialização do banco
│   └── database.db                 Banco de dados
|
├── docs
|   ├── estrutura_pastas.md
|   └── ambiente_virtual.md
|
├── frontend
|   └──
|
├── imagens [Repositório de imagens]
|   ├── Catalogos
│   |   ├── Linhas
│   |   ├── Padrao_Costura
│   |   └── Revestimentos
|   └── Identidade_visual
|
├── instance
|   
├── scripts
|   └──
|
├── statics
|   └──

├── templates                   Página HTML
│       ├── cliente.html
│       ├── consulta.html
│       ├── form_cliente.html
│       ├── form_veiculo.html
│       ├── lista_clientes.html
│       ├── ordem_servico.html
│       ├── 
│       ├──
|
├── app.py
│
├── README.md
|
├── venv                  Ambiente virtual [não versionado]
|
├── .gitignore 
|
└── requirements.txt      Lista de requisitos do ambiente virtual
```