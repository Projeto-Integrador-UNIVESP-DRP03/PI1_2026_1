# Detalhamento Técnico da Aplicação ZitOS

## 1. Identificação do projeto

**Nome:** ZitOS - Sistema de Gerenciamento de Ordens de Serviço

**Domínio:** Gestão operacional de tapeçaria automotiva.

**Objetivo:** Apoiar o cadastro de clientes e veículos, a elaboração de orçamentos, o acompanhamento de pedidos e a consulta de indicadores operacionais da Zito Tapeçaria para Autos.

**Contexto acadêmico:** Projeto Integrador I, desenvolvido no eixo de Computação da UNIVESP durante o primeiro semestre de 2026.

A aplicação substitui controles manuais ou dispersos por um sistema centralizado capaz de registrar dados de clientes, veículos, materiais, serviços, orçamentos e pedidos. O sistema também permite visualizar orçamentos, aprová-los ou recusá-los, acompanhar o status dos pedidos e gerar documentos PDF.

## 2. Arquitetura da solução

A solução utiliza uma arquitetura web monolítica, adequada ao porte atual do projeto. O backend e a camada de apresentação são mantidos no mesmo projeto e executados como uma aplicação Flask.

A arquitetura é composta pelas seguintes camadas:

- **Apresentação:** templates HTML renderizados pelo Jinja2.
- **Interação no navegador:** JavaScript próprio, modais, atualização parcial de listagens e chamadas assíncronas para o dashboard.
- **Aplicação:** rotas Flask organizadas em um Blueprint denominado `main`.
- **Persistência:** modelos SQLAlchemy mapeados para um banco SQLite.
- **Documentos:** geração de orçamento em PDF usando ReportLab.
- **Execução local:** servidor Flask para desenvolvimento e Waitress para a execução empacotada.
- **Distribuição:** PyInstaller, com arquivos `.spec` que incluem templates, arquivos estáticos e banco inicial.

O frontend não é uma SPA. A maior parte das páginas é renderizada no servidor, estratégia que reduz complexidade e é compatível com a natureza administrativa do sistema.

### 2.1 Estrutura principal

```text
sistema-tapecaria/
├── app/
│   ├── __init__.py       Application factory e configuração
│   ├── models.py         Modelos ORM e relacionamentos
│   └── routes.py         Rotas, regras de fluxo e geração de PDF
├── database/
│   ├── init.db.py        Recriação do banco em desenvolvimento
│   ├── migrate_integrity.py Migração de constraints
│   ├── seeds.py          Dados iniciais de clientes e veículos
│   └── seeds_catalogos.py Dados iniciais de catálogos
├── instance/
│   └── database.db      Banco SQLite local
├── static/
│   ├── css/estilo.css   Folhas de estilo
│   ├── js/modal.js       Gerenciamento de modais
│   └── imagens/          Identidade visual e catálogos
├── templates/            Interfaces HTML/Jinja
├── tests/                Testes automatizados
├── desktop.py            Entry point para Waitress/PyInstaller
├── app.py                Entry point web baseado na factory
├── requirements.txt      Dependências de execução e distribuição
├── requirements-dev.txt  Dependências de desenvolvimento e testes
├── SistemaTapecaria.spec Configuração alternativa de build
└── ZitOS.spec            Configuração principal de build
```

A pasta `frontend/` permanece vazia. O frontend efetivo está implementado em `templates/` e `static/`.

## 3. Linguagens e tecnologias

### 3.1 Linguagens

- **Python:** backend, regras de aplicação, persistência, scripts de banco, testes e geração de PDF.
- **HTML:** estrutura das páginas e formulários.
- **Jinja2:** composição dinâmica dos templates e uso de dados enviados pelas rotas.
- **CSS:** layout, responsividade, cores, tipografia e estados visuais.
- **JavaScript:** modais, foco, confirmações, filtros, paginação assíncrona e consumo do endpoint do dashboard.
- **SQL:** utilizado indiretamente pelo SQLAlchemy e diretamente nos scripts de inspeção/migração SQLite.
- **Markdown:** documentação técnica e operacional.

### 3.2 Frameworks e bibliotecas

As versões são controladas nos arquivos de requisitos do projeto. Entre os principais pacotes estão:

| Pacote | Versão registrada | Finalidade |
|---|---:|---|
| Flask | 3.1.3 | Framework web e roteamento |
| Flask-SQLAlchemy | 3.1.1 | Integração entre Flask e SQLAlchemy |
| SQLAlchemy | 2.0.48 | ORM e construção de consultas |
| Jinja2 | 3.1.6 | Templates server-side |
| Werkzeug | 3.1.6 | Utilitários Flask e hash de senhas |
| ReportLab | 4.4.10 | Geração de arquivos PDF |
| Pillow | 12.2.0 | Suporte a imagens durante empacotamento/uso de recursos |
| Waitress | 3.0.2 | Servidor WSGI para a distribuição desktop |
| PyInstaller | 6.19.0 | Empacotamento do aplicativo para Windows |
| pytest | 8.4.1 | Testes automatizados, em `requirements-dev.txt` |
| Chart.js | CDN | Gráficos do dashboard |
| Tailwind CSS | CDN | Utilitários visuais usados nos templates |
| Font Awesome | CDN | Ícones da interface |

As dependências visuais carregadas por CDN exigem acesso à internet para que todas as funcionalidades visuais sejam exibidas corretamente. O backend, o banco e os templates principais permanecem locais.

## 4. Funcionamento da aplicação

### 4.1 Inicialização

A inicialização recomendada utiliza `create_app()` em `app/__init__.py`. Essa função:

1. Cria a instância Flask.
2. Define os diretórios reais de templates e arquivos estáticos.
3. Cria a pasta `instance` quando necessário.
4. Configura a conexão SQLite.
5. Configura a chave de sessão e os cookies.
6. Registra a proteção CSRF.
7. Registra a exigência de autenticação.
8. Inicializa o SQLAlchemy.
9. Registra o Blueprint `main`.

O arquivo `app.py` utiliza essa mesma factory para execução web. O arquivo `desktop.py` configura os caminhos específicos do executável congelado, inicia o Waitress na interface `127.0.0.1` e abre o navegador local.

### 4.2 Autenticação e sessão

A autenticação implementada utiliza sessão assinada pelo Flask. O fluxo é:

1. O usuário acessa `/login`.
2. O formulário envia usuário, senha e token CSRF.
3. O backend compara o usuário com `ADMIN_USERNAME`.
4. A senha é validada por `check_password_hash()` contra `ADMIN_PASSWORD_HASH`.
5. Em caso de sucesso, a sessão é limpa e marcada como autenticada.
6. Um novo token CSRF é criado após o login.
7. Rotas protegidas redirecionam usuários não autenticados para `/login`.
8. `/logout` limpa a sessão por meio de uma requisição POST.

A senha não é armazenada em texto puro. O hash deve ser gerado com Werkzeug e configurado por variável de ambiente. A chave `SECRET_KEY` também deve ser configurada no ambiente, especialmente em produção.

### 4.3 Proteção CSRF

A aplicação gera um token por sessão e valida requisições `POST`, `PUT`, `PATCH` e `DELETE`. O token pode ser enviado em campo de formulário ou no cabeçalho `X-CSRF-Token`.

Os formulários renderizados pela base recebem o token automaticamente. O formulário de login, que não herda de `base.html`, contém o token explicitamente.

Essa proteção cobre operações como:

- cadastro e atualização de clientes;
- cadastro e atualização de veículos;
- criação e edição de orçamentos;
- exclusão lógica;
- aprovação e recusa de orçamento;
- alteração de status de pedidos;
- logout.

### 4.4 Fluxo de clientes e veículos

O usuário pode pesquisar um cliente por CPF/CNPJ ou código interno. Clientes ativos são listados com paginação e filtros por nome, código, placa, modelo e telefone.

No cadastro de cliente, são registrados:

- código do cliente;
- nome;
- telefone;
- endereço.

Um cliente pode possuir veículos. O cadastro de veículo normaliza a placa removendo caracteres não alfanuméricos e convertendo-a para letras maiúsculas. O backend valida a existência do cliente, a situação ativa, a unicidade da placa, a marca, o modelo e o ano.

A exclusão de clientes e veículos é lógica. O registro é marcado como inativo para preservar o histórico, embora dados de contato sejam removidos no fluxo de exclusão do cliente.

### 4.5 Fluxo de orçamentos

Um orçamento é associado a um veículo, que por sua vez pertence a um cliente. O formulário registra:

- data;
- quantidade de bancos;
- quantidade de apoios de cabeça;
- opções de bancos;
- manutenção do padrão original;
- logo prensada;
- troca de espuma;
- valor;
- observações;
- tecidos;
- costuras;
- cores.

O backend valida a relação entre veículo, cliente e orçamento. Quantidades e valores são validados antes da persistência. O valor é convertido para `Decimal` durante o parsing para evitar problemas comuns de ponto flutuante e aceita a notação monetária brasileira.

A atualização de um orçamento remove e recria os itens associados dentro da mesma transação, com `flush()` para obter o identificador de novos orçamentos sem confirmar parcialmente a operação.

As costuras são recebidas por ID, validadas contra o catálogo e gravadas com sua observação individual. O mesmo padrão é usado para tecidos e cores.

### 4.6 Fluxo de pedidos

A aprovação de um orçamento cria ou atualiza um pedido associado. O pedido possui estado operacional, podendo ser:

- `Pendente`;
- `Em Andamento`;
- `Concluído`;
- `Recusado` no fluxo de recusa.

Ao iniciar um pedido, a data de início pode ser preenchida. Ao concluí-lo, a data de conclusão é registrada. A associação entre pedido e orçamento possui índice único para impedir múltiplos pedidos para o mesmo orçamento.

### 4.7 Dashboard

O dashboard possui uma página HTML e um endpoint JSON em `/api/dashboard/stats`. O endpoint fornece indicadores como:

- total de clientes ativos;
- total de orçamentos;
- orçamentos convertidos;
- taxa de conversão;
- orçamentos do mês;
- valor de pedidos concluídos no mês;
- ticket médio;
- séries mensais para gráficos.

As séries mensais são limitadas aos últimos 12 meses para evitar crescimento indefinido da resposta e do processamento. O frontend utiliza `fetch()` para obter os dados e Chart.js para visualização.

### 4.8 Geração de PDF

A rota de PDF consulta orçamento, veículo, cliente e itens selecionados. O ReportLab monta o documento com:

- identidade visual;
- dados da empresa;
- dados do cliente;
- dados do veículo;
- serviços;
- materiais;
- observações;
- espaço para assinaturas.

O nome do arquivo é criado a partir de uma função de normalização de texto (`slugify`) e recebe o identificador do orçamento.

## 5. Persistência e modelo de dados

O banco principal é SQLite, localizado em `instance/database.db`. O acesso de aplicação é feito por SQLAlchemy ORM.

As entidades principais são:

- `clientes`;
- `telefones_cliente`;
- `emails_cliente`;
- `enderecos_cliente`;
- `veiculos`;
- `tecido`;
- `costura`;
- `cor`;
- `orcamento`;
- `orcamento_tecido`;
- `orcamento_costura`;
- `orcamento_cor`;
- `pedidos`.

Os relacionamentos de itens de orçamento utilizam chaves estrangeiras. O modelo atual torna essas relações obrigatórias para novas criações e define unicidade para `Pedido.id_orcamento`.

As conexões SQLite ativam `PRAGMA foreign_keys=ON`. Também foi criado o script `database/migrate_integrity.py`, que:

1. cria backup automático;
2. verifica registros com relações nulas;
3. verifica pedidos duplicados por orçamento;
4. reconstrói tabelas de associação com FKs obrigatórias;
5. cria o índice único de pedidos;
6. confirma a transação somente ao final.

A migração foi testada em uma cópia temporária do banco. O banco real não foi alterado durante o desenvolvimento desta etapa.

O banco físico ainda contém as tabelas legadas `espuma` e `orcamento_espuma`, que não estão representadas pelos modelos atuais. Essa divergência deve ser tratada por decisão de migração antes de uma limpeza estrutural.

## 6. Segurança implementada

Foram aplicadas as seguintes medidas:

- autenticação por sessão;
- senha armazenada como hash;
- configuração de credenciais por variáveis de ambiente;
- remoção de chave secreta fixa;
- debug desativado por padrão;
- proteção CSRF em métodos mutáveis;
- cookies de sessão com `HttpOnly`;
- política `SameSite=Lax`;
- opção de `Secure` via configuração;
- validação server-side de IDs, datas, quantidades e valores;
- verificação de registros ativos;
- verificação dos relacionamentos cliente/veículo/orçamento;
- prevenção de XSS em mensagens de modal com `textContent`;
- uso de `tojson` em argumentos de JavaScript nos templates;
- ativação de foreign keys do SQLite.

Essas medidas reduzem riscos, mas não substituem uma revisão de produção com HTTPS, gerenciamento de segredos, logs, backup e controle de acesso por perfis.

## 7. Interface e acessibilidade

A interface utiliza templates Jinja, CSS próprio, Tailwind via CDN e Font Awesome. As páginas possuem formulários, navegação lateral, listas paginadas, modais e feedback por mensagens flash.

Melhorias implementadas:

- labels e identificadores nos formulários existentes;
- mensagens de login com `role="alert"`;
- logout visível e acessível;
- modais com `role="dialog"`;
- atributo `aria-modal="true"`;
- associação de títulos por `aria-labelledby`;
- foco no primeiro botão ao abrir o modal;
- devolução do foco ao elemento anterior ao fechar;
- fechamento por tecla ESC;
- botões com `type` explícito em ações principais;
- confirmação de ações destrutivas por modal.

Ainda é recomendável executar uma avaliação formal com leitor de tela, navegação completa por teclado, medição automatizada de contraste e validação em dispositivos móveis.

## 8. JavaScript e APIs

O projeto não é uma SPA e não precisa ser transformado em uma para obter ganhos de usabilidade. O JavaScript é utilizado pontualmente para:

- abrir e fechar modais;
- confirmar exclusões e decisões de orçamento;
- manter foco em diálogos;
- buscar dados de CEP;
- carregar estatísticas do dashboard;
- atualizar tabelas e paginação em algumas telas;
- aplicar máscaras e interações de formulário.

Existe uma API interna para indicadores do dashboard:

```text
GET /api/dashboard/stats
```

Ela retorna JSON para consumo do Chart.js. Não foi criada uma API REST completa porque o sistema atual é principalmente server-side e não há necessidade comprovada de expor todas as entidades a clientes externos.

APIs futuras podem ser consideradas para:

- busca assíncrona de clientes e veículos em grandes volumes;
- integração com aplicativo móvel;
- integração com sistemas de pagamento;
- exportação controlada de relatórios;
- comunicação com serviços externos.

Cada API deverá possuir autenticação, autorização, validação, limitação de requisições e política de versionamento.

## 9. Testes e validação

Foi criada uma suíte em `tests/test_routes.py`, executada com pytest e banco temporário. Os testes cobrem:

- redirecionamento de usuários não autenticados;
- rejeição de credenciais inválidas;
- logout e limpeza de sessão;
- rejeição de POST sem CSRF;
- rejeição de data inválida em orçamento;
- persistência de costura e observação;
- criação de cliente;
- criação e normalização de veículo;
- bloqueio de transferência indevida de veículo;
- atualização de status e data de conclusão do pedido;
- exclusão de dados antigos dos gráficos do dashboard.

A última execução validada apresentou:

```text
11 passed
```

Também foram realizadas:

- compilação dos módulos Python com `py_compile`;
- verificação de erros no editor;
- validação de `PRAGMA foreign_keys=1`;
- execução da migração em cópia temporária;
- verificação de dependências com `pip install --dry-run`;
- verificação de existência do ícone do executável;
- verificação de ausência de caminhos absolutos no `ZitOS.spec`.

A checagem automática com `node --check` não foi executada porque Node.js não está instalado no ambiente disponível. O editor não reportou erros no arquivo JavaScript.

## 10. Execução local

A partir da pasta `sistema-tapecaria`, com o ambiente virtual ativo:

```powershell
python -m pip install -r requirements.txt
python database/init.db.py
python database/seeds.py
python database/seeds_catalogos.py
python app.py
```

A senha administrativa deve ser configurada antes do login:

```powershell
setx SECRET_KEY "UMA_CHAVE_LONGA_E_ALEATORIA"
setx ADMIN_USERNAME "admin"
setx ADMIN_PASSWORD_HASH "HASH_GERADO_COM_WERKZEUG"
```

O hash pode ser gerado com:

```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('SUA_SENHA'))"
```

Após `setx`, um novo terminal deve ser aberto para que as variáveis estejam disponíveis.

Para executar o modo desktop:

```powershell
python desktop.py
```

O modo desktop utiliza Waitress e abre o navegador em `http://127.0.0.1:5000`.

## 11. Banco e migrações

Para recriar o banco durante o desenvolvimento:

```powershell
python database/init.db.py
```

Esse comando executa `drop_all()` e apaga todos os dados. Deve ser usado somente em desenvolvimento ou em um banco descartável.

Para aplicar as constraints de integridade em um banco existente:

```powershell
python database/migrate_integrity.py
```

O script cria backup e interrompe a operação caso encontre relacionamentos nulos ou pedidos duplicados. A migração deve ser executada com a aplicação parada e deve ser validada antes de qualquer uso em produção.

## 12. Empacotamento para Windows

O empacotamento utiliza `ZitOS.spec`:

```powershell
pyinstaller --noconfirm ZitOS.spec
```

O resultado esperado é uma distribuição em `dist/ZitOS/`, contendo o executável, bibliotecas, templates, arquivos estáticos e o banco inicial.

A pasta completa deve ser distribuída. O banco utilizado em execução deve permanecer em uma localização persistente fora do diretório temporário `_MEIPASS`.

Antes da distribuição, devem ser configuradas as variáveis de ambiente de sessão e autenticação. Também é necessário testar o executável em uma máquina limpa e validar a criação, leitura e backup do banco.

## 13. Decisões técnicas

### 13.1 Flask monolítico

Foi mantido o monólito porque o volume atual e o número de usuários esperados não justificam microserviços, filas ou uma arquitetura distribuída. Essa decisão reduz custo operacional e facilita a implantação desktop.

### 13.2 Jinja e renderização server-side

A renderização server-side simplifica o fluxo de formulários e mantém as regras próximas das rotas. JavaScript é usado onde produz benefício claro, como modais, gráficos e atualizações parciais.

### 13.3 SQLite

SQLite é suficiente para uma instalação local ou de pequeno porte. Caso o sistema passe a ter múltiplos usuários concorrentes, acesso remoto ou necessidade de alta disponibilidade, PostgreSQL seria uma evolução mais adequada.

### 13.4 Waitress e PyInstaller

Waitress foi escolhido para substituir o servidor de desenvolvimento na distribuição local. PyInstaller permite entregar o sistema para Windows sem exigir Python instalado na máquina usuária.

## 14. Limitações e trabalho futuro

As seguintes atividades ainda devem ser consideradas antes de uma implantação mais ampla:

1. Definir perfis e permissões além do usuário administrativo único.
2. Aplicar a migração de integridade no banco oficial após backup e validação.
3. Decidir se as tabelas legadas de espuma serão mantidas, migradas ou removidas.
4. Adicionar logs estruturados, rotação e monitoramento de erros.
5. Implementar política de backup e restauração testada.
6. Executar auditoria formal de acessibilidade.
7. Testar o executável em máquina limpa.
8. Avaliar dependências externas carregadas por CDN.
9. Criar migrações versionadas para futuras alterações do schema.
10. Adicionar testes de geração de PDF, autorização, concorrência e todos os fluxos de erro.
11. Considerar índices adicionais após medir consultas reais em bases maiores.
12. Preparar HTTPS, domínio, armazenamento e banco gerenciado caso o sistema seja convertido para hospedagem em nuvem.

## 15. Conclusão

O ZitOS é uma aplicação web monolítica de pequeno porte, com backend Python/Flask, persistência SQLite e frontend server-side em Jinja. Durante a evolução técnica foram corrigidos problemas de configuração, segurança, persistência, validação, integridade referencial, compatibilidade com SQLAlchemy, acessibilidade básica, documentação, desempenho e testes.

O projeto possui uma base funcional adequada para uso local controlado. A próxima evolução deve concentrar-se na aplicação da migração no banco oficial, no fortalecimento de autorização e observabilidade, na expansão da cobertura de testes e na validação do processo de distribuição para Windows.
