# Relatório acadêmico de validação funcional do Sistema Tapecaria

## 1. Introdução

Este relatório apresenta a execução da suíte de testes automatizados do Sistema Tapecaria com foco em rotas, autenticação, regras de negócio e persistência de dados. O objetivo é demonstrar que a aplicação mantém comportamento esperado em cenários críticos de uso, permitindo avaliar conformidade funcional sob condições controladas de teste.

A execução foi realizada no ambiente de desenvolvimento do projeto, com o uso do framework pytest e da infraestrutura de testes do Flask. Os cenários avaliados cobrem fluxos de acesso, operações de clientes, orçamentos, veículos, pedidos e dashboard, além de validações de diagnóstico do banco de dados.

## 2. Objetivo

O presente documento tem por finalidade registrar, de forma acadêmica e reusável, os resultados obtidos por meio da suíte de testes do projeto. A análise considera:

- validação da usabilidade funcional das rotas;
- verificação da segurança da autenticação e da sessão;
- confirmação das regras de negócio em clientes, orçamentos e pedidos;
- checagem da persistência em banco SQLite temporário;
- avaliação do estado final de conformidade do sistema.

## 3. Metodologia

A metodologia adotada foi a de testes de integração por rota, executados pela biblioteca pytest em ambiente isolado.

### Ambiente de execução

- Python: 3.13.5
- pytest: 8.3.4
- Flask: 3.1.3
- Banco de testes: SQLite em memória
- Comando executado: `python -m pytest -q`

### Cobertura funcional

A suíte avalia os seguintes domínios:

- autenticação e segurança;
- clientes e busca;
- orçamentos;
- veículos e pedidos;
- dashboard;
- diagnóstico de banco de dados.

## 4. Resultados

A execução foi concluída com sucesso. Os indicadores observados foram:

| Indicador | Valor |
|---|---:|
| Testes executados | 33 |
| Testes aprovados | 33 |
| Testes falhos | 0 |
| Testes ignorados | 0 |
| Tempo de execução | 13,52 segundos |

Os testes aprovados incluem validações de:

- redirecionamento de usuários não autenticados;
- rejeição de login com credenciais inválidas;
- encerramento correto da sessão;
- proteção CSRF em ações sensíveis;
- criação, busca e inativação de clientes;
- validação e persistência de orçamentos;
- aprovação e rejeição de orçamentos;
- geração de PDF de orçamento;
- cadastro e atualização de veículos;
- controle de status e conclusão de pedidos;
- indicadores de dashboard e filtros temporais;
- diagnóstico de banco de dados.

## 5. Interpretação dos resultados

Os resultados demonstram que a aplicação atende aos fluxos principais de uso previstos pela suíte automatizada. A ausência de falhas indica que o sistema manteve integridade funcional nas operações avaliadas e que as regras de autenticação, validação e persistência preservaram seu comportamento ao longo dos cenários testados.

Mesmo com a conformidade funcional demonstrada, a validade da suíte depende da continuidade da manutenção dos testes e da atualização das premissas quando o sistema evolui. Nesse sentido, a suíte funciona como um mecanismo de proteção contra regressões e serve como documentação comportamental da aplicação.

## 6. Conclusão

A execução da suíte de testes do Sistema Tapecaria foi considerada conforme ao objetivo da validação funcional. O projeto apresentou 33 testes executados, 33 aprovados e 0 falhas, confirmando a estabilidade dos fluxos críticos da aplicação no ambiente de teste empregado.

Esse resultado reforça a maturidade da implementação atual e torna a suíte relevante como evidência de qualidade para uso em documentação acadêmica, relatórios de acompanhamento e validação do processo de desenvolvimento.

### Artefato gerado

- Relatório HTML: `reports/relatorio-testes.html`
- Documento acadêmico: `docs/relatorio_academico_testes.md`
