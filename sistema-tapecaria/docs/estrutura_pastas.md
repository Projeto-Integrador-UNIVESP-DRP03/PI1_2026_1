# Estrutura de pastas do Sistema

```text
sistema-tapecaria/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask e configuração global
│   ├── models.py            # Modelos SQLAlchemy e relacionamentos
│   └── routes.py            # Rotas, regras de negócio e geração de PDF
│
├── database/
│   ├── init.db.py           # Recriação do banco em desenvolvimento
│   ├── migrate_integrity.py # Correção/validação de integridade do banco
│   ├── seeds.py             # Dados iniciais de clientes e veículos
│   └── seeds_catalogos.py  # Catálogos de tecidos, costuras e cores
│
├── docs/
│   ├── ambiente_virtual.md
│   ├── aplicativo.md
│   ├── criacao_recriacao_db.md
│   ├── detalhamento_tecnico.md
│   ├── estrutura_pastas.md
│   ├── modais.md
│   ├── protecao_app.md
│   ├── seeds.md
│   └── teste_rotas.md
│
├── instance/
│   └── database.db          # Banco principal da aplicação em SQLite
│
├── reports/
│   └── relatorio-testes.html
│
├── scratch/
│   ├── clear_records.py
│   └── update_db.py
│
├── scripts/
│   └── (diretório reservado para utilitários e automações futuras)
│
├── static/
│   ├── css/
│   │   ├── estilo.css
│   │   ├── form_cliente.css
│   │   ├── lista_clientes.css
│   │   ├── lista_orcamentos.css
│   │   ├── pedidos.css
│   │   └── pedidos_concluidos.css
│   ├── js/
│   │   └── modal.js
│   └── imagens/
│       ├── Catalogos/
│       └── Identidade_visual/
│
├── templates/
│   ├── base.html
│   ├── cliente.html
│   ├── consulta.html
│   ├── dashboard.html
│   ├── form_cliente.html
│   ├── form_orcamento.html
│   ├── form_veiculo.html
│   ├── lista_clientes.html
│   ├── lista_orcamentos.html
│   ├── login.html
│   ├── modais_preview.html
│   ├── pedido_editar.html
│   ├── pedidos.html
│   ├── pedidos_concluidos.html
│   ├── selecionar_cliente_pedido.html
│   ├── selecionar_veiculo_pedido.html
│   └── visualizar_orcamento.html
│
├── tests/
│   ├── README.md
│   └── test_routes.py
│
├── .gitignore
├── .pytest_cache/
├── README.MD
├── SistemaTapecaria.spec
├── ZitOS.spec
├── app.py
├── desktop.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── venv/                     # ambiente virtual local, não versionado
├── build/                    # artefatos de empacotamento locais
├── dist/                     # saída do PyInstaller
├── frontend/                 # diretório legado, mantido para expansão futura
├── __pycache__/
└── Tapeçaria.zip            # artefato auxiliar local
``` 
```

## Observações

- A aplicação é organizada como um projeto Flask monolítico, com backend, templates e arquivos estáticos em diretórios separados.
- A pasta `instance/` guarda o banco SQLite em execução e deve ser preservada para persistência local.
- As pastas `build/`, `dist/`, `reports/` e `.pytest_cache/` são artefatos locais gerados pela execução do sistema e dos testes.
- O diretório `scratch/` contém scripts de manutenção e suporte, e não faz parte do fluxo principal da aplicação.
