# Testes do Sistema Tapecaria

## Objetivo

Este diretório reúne a suíte de testes automatizados da aplicação Flask, implementada com `pytest`. Os testes validam o comportamento real das rotas usando uma instância da aplicação com banco SQLite temporário, sem mocks da lógica de negócio.

## Execução

A partir da pasta raiz do projeto, execute:

```powershell
pytest tests/test_routes.py
```

Também é possível rodar toda a suíte da pasta de testes:

```powershell
pytest
```

A execução gera relatório HTML em `reports/relatorio-testes.html` quando o processo de geração do relatório estiver ativado no ambiente do projeto.

## Cobertura atual implementada

O arquivo `test_routes.py` cobre os principais fluxos da aplicação:

- Autenticação e segurança:
  - acesso sem login redirecionado para `/login`;
  - login inválido rejeitado;
  - logout limpando a sessão;
  - rejeição de requisições sem CSRF;
  - validação de hash de senha mal formatado.

- Clientes e busca:
  - busca por cliente;
  - listagem de clientes ativos;
  - cadastro e atualização do cadastro;
  - exclusão lógica de cliente e veículos relacionados;
  - validação da renderização de dados com caracteres especiais.

- Orçamentos:
  - criação com dados válidos e inválidos;
  - persistência de itens de costura e observações;
  - aprovação e recusa do orçamento;
  - geração de PDF do orçamento;
  - listagem da página de orçamentos.

- Veículos e pedidos:
  - normalização da placa;
  - validação de associação ao cliente correto;
  - edição do cadastro do veículo;
  - atualização de status dos pedidos;
  - busca de pedidos por nome do cliente;
  - listagem de pedidos concluídos.

- Dashboard:
  - filtros de dados por período;
  - cálculo e retorno do payload JSON utilizado nos gráficos.

## Estrutura

- `test_routes.py`: suíte principal de testes de rotas e regras de negócio.
- Fixtures internas: cada teste cria um app e banco temporário para isolar cenários.

## Boas práticas adotadas

- Cada teste utiliza base isolada com `tmp_path`.
- As verificações validam respostas HTTP, redirecionamentos e dados persistidos.
- O cenário de negócio é testado de forma realista, sem dependência de implementação interna.
- A suíte é organizada por blocos temáticos para facilitar manutenção e evolução.

## Observação

Os relatórios gerados pela execução dos testes não devem ser versionados junto ao código-fonte, sendo mantidos como artefato de execução local ou de CI.
