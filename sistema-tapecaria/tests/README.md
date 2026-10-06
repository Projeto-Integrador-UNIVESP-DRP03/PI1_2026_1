# Testes do Sistema Tapecaria

## Objetivo

Este diretório contém os testes de integração de rotas da aplicação Flask. Os testes usam uma aplicação real com um banco SQLite temporário, sem mocks da lógica de negócio.

## Execução

Execute a suíte a partir da raiz do projeto:

```powershell
pytest tests/test_routes.py
```

O comando gera um relatório HTML autocontido em `reports/relatorio-testes.html`.

## Estrutura

- `test_routes.py`: testes de autenticação, clientes, orçamentos, veículos, pedidos e dashboard.
- As fixtures vivem no próprio arquivo de testes para manter a suíte autocontida.

## Regras

- Cada teste deve isolar o estado com uma base temporária.
- As asserções devem validar o comportamento real da rota e o estado persistido.
- Os testes devem representar um cenário de negócio, não detalhes internos da implementação.
- Não inclui arquivos de relatório gerados na versão do código.
