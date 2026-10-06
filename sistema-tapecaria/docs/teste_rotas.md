# Documentação dos testes de rotas do Sistema Tapecaria

## 1. Propósito da documentação

Este documento apresenta a suíte de testes de rotas do Sistema Tapecaria, explica o que cada teste valida e descreve o resultado obtido no relatório de execução.

O objetivo é permitir que desenvolvedores que não trabalham diretamente com testes compreendam:

- o que a aplicação deve fazer;
- quais fluxos são protegidos ou podem falhar;
- por que cada teste é importante;
- como os testes são executados;
- como interpretar o resultado do relatório;
- quais pontos do sistema são cobertos pela suíte.

A documentação considera o ponto de vista do desenvolvedor de aplicação, não apenas do responsável pelos testes.

---

## 2. O que é uma suíte de testes de rotas

Uma suíte de testes de rotas verifica o comportamento da aplicação por meio das URLs que o usuário acessa. Em vez de testar apenas funções internas, os testes executam o sistema como se fossem usados em um navegador e em um servidor real.

No caso do Sistema Tapecaria, um teste de rota pode:

- enviar uma requisição HTTP;
- verificar o código de resposta;
- verificar uma redireção;
- verificar o conteúdo da página;
- confirmar que dados foram persistidos no banco;
- confirmar que um usuário foi autenticado ou desconectado;
- verificar que uma ação proibida foi rejeitada.

Esse tipo de teste é importante porque o aplicativo pode apresentar o comportamento correto em uma função, mas ainda falhar lorsque essa função é acessada por uma rota, quando há um mecanismo de sessão, quando o banco aceita os dados ou quando a página está autenticada.

---

## 3. Tipo de testes utilizados

A suíte utiliza **testes de integração por rota**. Cada teste executa a aplicação Flask por meio do cliente de teste do Flask, sem iniciar um servidor externo. Assim, o teste verifica a interação entre a rota, o template, a sessão, o banco e as regras de negócio.

A classificação dos testes atuais é a seguinte:

| Classificação | O que é validado | Exemplo |
|---|---|---|
| Integração por rota | A requisição, a resposta e a interação entre os componentes da aplicação | Acesso a `/clientes` após login |
| Segurança | Autenticação, sessão, redirecionamento e proteção CSRF | Login inválido ou requisição sem token |
| Regra de negócio | Regras sobre clientes, veículos, pedidos e orçamentos | Inativação de cliente e atualização de status |
| Validação de entrada | Formatos e valores recebidos pelo sistema | Data inválida ou placa mal formatada |
| Apresentação | Conteúdo renderizado na página | Formulário de edição ou lista de pedidos |
| Persistência | Alterações gravadas no banco SQLite temporário | Criação de cliente ou orçamento |

A suíte não utiliza mocks da lógica da aplicação. Isso significa que o comportamento real de login, banco, páginas, formulários e rotas é exercitado. Os testes apresentam uma classificação principal de integração por rota, mas podem também cobrir regras de segurança, validação, apresentação e persistência no mesmo cenário.

### Classificação por domínio

- **Autenticação e segurança:** testes de sessão, login, logout, redirecionamento e CSRF.
- **Clientes e busca:** testes de integração, regras de negócio e persistência de clientes.
- **Orçamentos:** testes de validação, persistência, fluxo de negócio e geração de PDF.
- **Veículos e pedidos:** testes de integração, regras de negócio, apresentação e estado do pedido.
- **Dashboard:** teste de filtragem temporal e integração com o endpoint de estatísticas.

> Os testes não são testes unitários isolados de funções internas. Eles são testes de integração por rota, com pequenas verificações de regras de negócio dentro de cada cenário.

---

## 4. Organização da suíte

A suíte está distribuída em cinco grupos de domínio:

| Domínio | Quantidade de testes | Responsabilidade principal |
|---|---:|---|
| Autenticação e segurança | 4 | Login, logout, acesso anônimo e proteção CSRF |
| Clientes e busca | 5 | Busca, listagem, cadastro, atualização e inativação |
| Orçamentos | 6 | Validação, persistência, aprovação, rejeição e geração de PDF |
| Veículos e pedidos | 8 | Cadastro, atualização, busca e controle de pedidos |
| Dashboard | 1 | Indicadores e filtros temporais |
| Testes de acesso inicial | 3 | Redirecionamento, login inválido e logout |

No total, a suíte possui **27 testes**. A contagem considera os três testes de acesso inicial, além dos grupos de domínio listed acima.

Os testes de acesso inicial aparecem antes dos grupos por domínio porque representam os controles básicos da aplicação e são reutilizados como exemplos do fluxo de sessão.

---

## 5. Preparação do ambiente de teste

Antes de cada teste, a fixture de aplicação cria uma instância da aplicação com:

- modo de teste ativado;
- banco SQLite temporário;
- usuário administrator com uma senha de teste;
- cliente inicial;
- veículo inicial;
- uma costura inicial.

O banco é criado e removido dentro de cada teste. Essa isolação evita que dados inserted em um teste permaneçam disponíveis em outro e garante que o resultado não dependa da ordem de execução.

O cliente autenticado também é preparado por uma fixture própria. Ele faz login com o usuário administrator e mantém a sessão ativa para que as rotas protegidas sejam verificadas como um usuário real.

---

## 6. Testes de autenticação e segurança

### 6.0. Testes de acesso inicial

Os três testes abaixo correspondem aos testes executados antes dos grupos de domínio e validam os controles básicos da sessão.

#### 6.0.1. Acesso anônimo é redirecionado para o login

**Teste:** `test_unauthenticated_user_is_redirected_to_login`

**Tipo:** teste de integração de autenticação.

**O que valida:**

O usuário que ainda não autenticou tenta acessar a página inicial. O sistema deve retornar um redirecionamento para a página de login e preservar a página desejada no parâmetro `next`.

**Importância:**

Esse teste garante que páginas protegidas não fiquem acessíveis sem autenticação. A aplicação evita divulgar informações de clientes, veículos, orçamentos e pedidos a usuários anônimos.

**Resultado esperado:**

- status HTTP 302;
- localização para `/login?next=/`.

#### 6.0.2. Login com credenciais inválidas é rejeitado

**Teste:** `test_invalid_login_is_rejected`

**Tipo:** teste de integração de autenticação.

**O que valida:**

O usuário fornece uma senha incorreta. Não deve ser autenticado e deve receber a página de login novamente.

**Importância:**

Esse teste protege a aplicação contra uso de credenciais inválidas e garante que a sessão não seja considerada autenticada mesmo quando a resposta HTTP seja recebida.

**Resultado esperado:**

- status HTTP 200;
- a sessão não possui o atributo de autenticação.

#### 6.0.3. Logout encerra a sessão

**Teste:** `test_logout_clears_session`

**Tipo:** teste de sessão e autenticação.

**O que valida:**

Um usuário autenticado envia uma requisição de logout. A aplicação deve remover a sessão e redirecionar para a página de login.

**Importância:**

Esse teste evita que experiências antigas permaneçam acessíveis depois que o usuário encerra a sessão.

**Resultado esperado:**

- status HTTP 302;
- localização para `/login`.

### 6.1. Testes de autenticação organizados na classe

Os testes seguintes foram reorganizados na classe `TestAutenticacaoESeguranca`. Eles exercitam os mesmos cenários de sessão, mas estão separados dos testes de acesso inicial para facilitar a leitura e a manutenção da suíte.

#### 6.1.1. Acesso anônimo é redirecionado para o login

**Teste:** `test_unauthenticated_user_is_redirected_to_login`

**Tipo:** teste de integração de autenticação.

**O que valida:** o usuário sem sessão deve receber redirecionamento para o login.

**Importância:** mantém a proteção das páginas sensíveis.

#### 6.1.2. Login com credenciais inválidas é rejeitado

**Teste:** `test_invalid_login_is_rejected`

**Tipo:** teste de integração de autenticação.

**O que valida:** credenciais incorretas não devem criar uma sessão autenticada.

**Importância:** impede o acesso com informações inválidas.

#### 6.1.3. Logout encerra a sessão

**Teste:** `test_logout_clears_session`

**Tipo:** teste de sessão e autenticação.

**O que valida:** o logout remove a sessão e redireciona ao login.

**Importância:** garante que a sessão não permaneça ativa após o encerramento.

#### 6.1.4. Requisição sem CSRF é rejeitada

**Teste:** `test_post_without_csrf_is_rejected`

**Tipo:** teste de segurança e proteção contra requisições maliciosas.

**O que valida:** uma requisição POST protegida sem token CSRF deve ser rejeitada com status 400.

**Importância:** impede ações maliciosas em nome do usuário.

**Resultado esperado:**

- status HTTP 400.

---

## 7. Testes de clientes e busca

### 7.1. Busca de cliente existente

**Teste:** `test_customer_search_finds_existing_client`

**Tipo:** teste de integração de busca.

**O que valida:**

O usuário envia o código de cliente e obtém a página de resultado. A aplicação deve encontrar o cliente inicial e exibir seu nome.

**Importância:**

Esse teste garante que a rota de busca está conectada ao banco e que o código enviado pelo usuário corresponde ao cliente correto.

**Resultado esperado:**

- status HTTP 200;
- o nome do cliente aparece na resposta.

### 7.2. Listagem oculta clientes inativos

**Teste:** `test_client_list_hides_inactive_clients`

**Tipo:** teste de regra de negócio e integração.

**O que valida:**

Um cliente é inserido no banco com o status inativo. A página de clientes deve continuar exibindo o cliente ativo, mas não deve mostrar o cliente inativo.

**Importância:**

Esse teste protege a regra de que clientes inativos não devem aparecer como opções válidas na aplicação. Ele também evita que a interface seja alterada por dados que não devem estar disponíveis.

**Resultado esperado:**

- status HTTP 200;
- o cliente ativo aparece;
- o cliente inativo não aparece.

### 7.3. Cadastro de cliente

**Teste:** `test_client_creation_redirects_to_vehicle_form`

**Tipo:** teste de criação e integração.

**O que valida:**

O usuário envia o nome, o código e o telefone do cliente. A aplicação deve criar o cliente no banco e redirecionar para a etapa de cadastro do veículo.

**Importância:**

Esse teste garante que o formulário de cliente funciona, que os dados são persistidos e que o fluxo continua para a próxima etapa do processo.

**Resultado esperado:**

- status HTTP 302;
- o cliente está no banco com os dados enviados;
- o telefone está associado ao cliente.

### 7.4. Atualização de cliente

**Teste:** `test_client_update_changes_name_and_phone`

**Tipo:** teste de atualização e integração.

**O que valida:**

O usuário altera o nome, o telefone e os dados de endereço do cliente. A aplicação deve salvar as alterações no banco.

**Importância:**

Esse teste garante que a atualização de cliente não apenas modifica a página, mas também persiste corretamente as mudanças. Ele também valida a associação de endereço e telefone.

**Resultado esperado:**

- status HTTP 302;
- o nome e o telefone foram alterados;
- a cidade do endereço foi atualizada.

### 7.5. Exclusão suave de cliente

**Teste:** `test_customer_soft_delete_hides_client_and_vehicle`

**Tipo:** teste de regra de negócio, inativação e integração.

**O que valida:**

O cliente é marcado como inativo, assim como o veículo associado. A página de clientes deve esconder o cliente.

**Importância:**

A exclusão suave é importante porque ela preserva o histórico do cliente e do veículo. O sistema pode manter os dados, mas ele não deve mais apresentá-los como ativos.

**Resultado esperado:**

- status HTTP 302;
- o cliente está com `cliente_ativo = 0`;
- o veículo está com `veiculo_ativo = 0`;
- o cliente não aparece na listagem.

---

## 8. Testes de orçamentos

### 8.1. Data de orçamento inválida

**Teste:** `test_invalid_budget_date_is_redirected_without_creation`

**Tipo:** teste de validação de entrada e integração.

**O que valida:**

O usuário envia uma data inválida. A aplicação deve rejeitar o valor e não criar um item de costura ou orçamento.

**Importância:**

Esse teste protege o sistema contra dados malformados e evita que registros inválidos sejam persistidos. Ele também garante que a aplicação não aceite informações que não podem ser processadas.

**Resultado esperado:**

- status HTTP 302;
- nenhum item de costura é criado.

### 8.2. Persistência de costura e observação

**Teste:** `test_budget_saves_costura_and_observation`

**Tipo:** teste de integração e persistência.

**O que valida:**

O usuário cadastra um orçamento com uma costura e uma observação. A aplicação deve guardar a relação entre o orçamento e a costura.

**Importância:**

Esse teste garante que as informações adicionais do orçamento, como a observação da costura, sejam armazenadas corretamente. A observação também ajuda a equipe a entender o contexto da configuração.

**Resultado esperado:**

- status HTTP 302;
- um item de `OrcamentoCostura` é criado;
- a costura e a observação estão associadas corretamente.

### 8.3. Aceitação do orçamento

**Teste:** `test_budget_acceptance_creates_pending_order`

**Tipo:** teste de fluxo de negócio e integração.

**O que valida:**

O usuário aceita um orçamento. O sistema deve criar um pedido com o status `Pendente` e indicar que o cliente aceitou o orçamento.

**Importância:**

Esse teste garante que a decisão do cliente seja convertida em um pedido válido. O pedido funciona como a próxima etapa do processo e precisa manter o histórico da decisão.

**Resultado esperado:**

- status HTTP 302;
- um pedido existe para o orçamento;
- `boolean_aceite_cliente` é verdadeiro;
- o status é `Pendente`.

### 8.4. Rejeição do orçamento

**Teste:** `test_budget_refusal_creates_rejected_order`

**Tipo:** teste de fluxo de negócio e integração.

**O que valida:**

O usuário rejeita um orçamento. O sistema deve criar um pedido com o status `Recusado`.

**Importância:**

Esse teste garante que a rejeição do cliente seja registrada corretamente. O sistema deve distinguir a rejeição de um pedido ainda pendente.

**Resultado esperado:**

- status HTTP 302;
- um pedido existe para o orçamento;
- `boolean_aceite_cliente` é falso;
- o status é `Recusado`.

### 8.5. Listagem de orçamentos

**Teste:** `test_budget_list_page_renders_successfully`

**Tipo:** teste de apresentação da página e integração.

**O que valida:**

O usuário acessa a página de listagem de orçamentos. A aplicação deve responder com sucesso e mostrar a estrutura da página.

**Importância:**

Esse teste garante que a rota de listagem existe e que o template é renderizado com os elementos esperados. Ele também detecta problemas de integração entre rota, banco e template.

**Resultado esperado:**

- status HTTP 200;
- a página é renderizada;
- o campo de busca ou o título esperado está disponível.

### 8.6. Download do PDF do orçamento

**Teste:** `test_budget_pdf_download_returns_pdf_response`

**Tipo:** teste de integração e formato de documento.

**O que valida:**

O usuário acessa o PDF de um orçamento existente. A aplicação deve retornar um documento PDF e um cabeçalho de download.

**Importância:**

Esse teste garante que o orçamento possa ser exportado e que o arquivo tenha o formato correto. O PDF é um entregável utilizado pelo usuário e deve ser disponibilizado com o nome e o tipo corretos.

**Resultado esperado:**

- status HTTP 200;
- mime type `application/pdf`;
- cabeçalho de `Content-Disposition` com o nome do arquivo.

---

## 9. Testes de veículos e pedidos

### 9.1. Criação de veículo com placa normalizada

**Teste:** `test_vehicle_creation_normalizes_plate`

**Tipo:** teste de validação de dados e integração.

**O que valida:**

O usuário envia uma placa em letras minúsculas e com caracteres especiais. A aplicação deve normalizar a placa e salvar a forma padronizada.

**Importância:**

A normalização evita diferenças entre `ABC1234`, `abc-1234` e `ABC-1234`. Isso reduz conflitos no banco e garante que a identificação do veículo seja consistente.

**Resultado esperado:**

- status HTTP 302;
- a placa foi salva como `ABC1234`;
- o veículo foi associado ao cliente correto.

### 9.2. Veículo não pode ser assinalado a outro cliente

**Teste:** `test_vehicle_cannot_be_assigned_to_another_client`

**Tipo:** teste de regra de negócio e integração.

**O que valida:**

O usuário tenta alterar o cliente associado a um veículo. A aplicação deve manter o cliente original.

**Importância:**

Essa regra evita que um veículo seja transferido acidentalmente e garante que a associação entre cliente e veículo permaneça correta.

**Resultado esperado:**

- status HTTP 302;
- o `id_cliente` do veículo permanece igual ao cliente original.

### 9.3. Página de edição do veículo

**Teste:** `test_vehicle_edit_page_renders_form`

**Tipo:** teste de renderização da página e integração.

**O que valida:**

O usuário acessa a página de edição do veículo existente. A aplicação deve retornar o formulário de atualização.

**Importância:**

Esse teste garante que a rota de edição está disponível e que a página contém os elementos necessários para alterar o veículo.

**Resultado esperado:**

- status HTTP 200;
- o formulário de edição é renderizado.

### 9.4. Atualização do veículo

**Teste:** `test_vehicle_update_changes_info`

**Tipo:** teste de atualização e integração.

**O que valida:**

O usuário altera a placa, a marca, o modelo e a cor do veículo. A aplicação deve salvar as mudanças e normalizar a placa.

**Importância:**

Esse teste garante que os dados do veículo sejam atualizados no banco e que a informação apresentada ao usuário corresponda ao conteúdo persistido.

**Resultado esperado:**

- status HTTP 302;
- a placa, a marca, o modelo e a cor foram alterados corretamente.

### 9.5. Busca de pedidos por nome do cliente

**Teste:** `test_pedido_search_filters_by_customer_name`

**Tipo:** teste de filtragem e integração.

**O que valida:**

O usuário procura um pedido usando o nome do cliente. A aplicação deve retornar o pedido correspondente.

**Importância:**

Esse teste garante que a busca de pedidos funciona e que os dados do cliente estão relacionados ao pedido corretamente.

**Resultado esperado:**

- status HTTP 200;
- o nome do cliente aparece na resposta.

### 9.6. Listagem de pedidos concluídos

**Teste:** `test_completed_orders_page_lists_concluded_orders`

**Tipo:** teste de filtragem e integração.

**O que valida:**

O usuário acessa a página de pedidos concluídos. A aplicação deve listar um pedido com o status `Concluído` e data de conclusão.

**Importância:**

Esse teste garante que a aplicação diferencie os pedidos ativos dos pedidos concluídos e que o histórico seja apresentado corretamente.

**Resultado esperado:**

- status HTTP 200;
- o cliente associado ao pedido concluído aparece na página.

### 9.7. Conclusão do pedido

**Teste:** `test_order_status_sets_completion_date`

**Tipo:** teste de estado e integração.

**O que valida:**

O pedido pendente é marcado como concluído. A aplicação deve atualizar o status e registrar a data de conclusão.

**Importância:**

Esse teste garante que o ciclo de vida do pedido seja completo. A data de conclusão permite acompanhar quando o processo terminou.

**Resultado esperado:**

- status HTTP 302;
- o status é `Concluído`;
- a data de conclusão não é nula.

### 9.8. Status de pedido inválido

**Teste:** `test_invalid_order_status_is_rejected`

**Tipo:** teste de validação de estado e integração.

**O que valida:**

O usuário envia um status inválido para uma requisição de atualização do pedido. O sistema deve manter o status anterior.

**Importância:**

Esse teste evita que valores desconhecidos sejam gravados no banco e garante que apenas os estados permitidos existam.

**Resultado esperado:**

- status HTTP 302;
- o status continua `Pendente`.

---

## 10. Teste do dashboard

### 10.1. Gráfico ignora orçamentos antigos

**Teste:** `test_dashboard_chart_ignores_budget_older_than_twelve_months`

**Tipo:** teste de filtragem temporal e integração.

**O que valida:**

O dashboard recebe um orçamento antigo e um orçamento recente. A aplicação deve incluir apenas o orçamento recente no gráfico.

**Importância:**

O dashboard precisa mostrar informações atuais e relevantes. Orçamentos antigos podem distorcer os indicadores e oferecer uma visão equivocada do desempenho do sistema.

**Resultado esperado:**

- status HTTP 200;
- a etiqueta do mês atual está presente;
- a etiqueta do mês antigo não está presente.

---

## 11. Como os testes são executados

A execução da suíte deve ser feita a partir da raiz do projeto:

```powershell
pytest tests/test_routes.py
```

O comando utiliza a configuração de [pytest.ini](../pytest.ini), que gera o relatório HTML automaticamente.

O relatório fica em:

```text
reports/relatorio-testes.html
```

O relatório é um artefato de execução e não deve ser versionado. Isso evita que arquivos gerados em uma máquina sejam incluídos no código do projeto.

---

## 12. Resultado do relatório

A execução validada apresentou os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Testes executados | 27 |
| Testes aprovados | 27 |
| Testes falhas | 0 |
| Testes ignorados | 0 |
| Tempo de execução | 8,43 segundos |
| Relatório | `reports/relatorio-testes.html` |

O relatório informou que todos os testes passaram. Isso significa que os cenários de autenticação, clientes, orçamentos, veículos, pedidos e dashboard foram executados sem falhas.

O resultado não significa que o sistema esteja completamente sem problemas. Ele indica que a suíte atual cobrem os fluxos testados e que os testes não encontraram falhas nos cenários avaliados.

---

## 13. Como interpretar o relatório

O relatório HTML apresenta:

- resumo geral da execução;
- ambiente de execução, incluindo Python e pytest;
- tabela dos testes;
- status de cada teste;
- tempo de execução;
- logs e detalhes quando ocorre uma falha;
- filtros para mostrar testes aprovados, falhas, ignorados e demais estados.

Para um teste aprovado, o status deve aparecer como `Passed` e o resultado deve ser verde.

Para um teste falho, o relatório deve mostrar:

- o nome do teste;
- a mensagem de falha;
- a resposta HTTP ou o valor incorreto;
- o log associado ao teste;
- a tela de traceback, quando disponível.

Um teste falho deve ser analisado antes da próxima entrega. A causa deve ser identificada e corrigida antes de considerar a suíte validada.

---

## 14. Importância dos testes para o projeto

Os testes têm uma importância fundamental para o desenvolvimento do Sistema Tapecaria:

1. **Proteção contra regressões:** alterações em uma rota pode quebrar outra operação.
2. **Validação do comportamento real:** os testes exercitam a aplicação como o usuário a utiliza.
3. **Segurança:** autenticação, sessão e CSRF são verificadas.
4. **Rastreabilidade:** dados de clientes, veículos, orçamentos e pedidos são confirmados no banco.
5. **Redução do risco de entrega:** falhas são detectadas antes da distribuição.
6. **Menos tempo de manutenção:** problemas recorrentes são identificados rapidamente.
7. **Maior clareza do fluxo:** cada domínio possui testes específicos e compreensíveis.
8. **Documentação do comportamento:** os testes registram o que a aplicação deve fazer.

---

## 15. Conclusão

A suíte de testes de rotas do Sistema Tapecaria cobre os fluxos principais da aplicação. A execução atual apresentou 27 testes aprovados, sem falhas.

A documentação deste arquivo foi criada para facilitar a compreensão desses testes pelos desenvolvedores e para mostrar quando cada teste deve ser considerado um ponto de proteção importante no processo de desenvolvimento.

Para manter a suíte útil, é recomendável executar os testes após cada alteração funcional e revisar o relatório antes de entregar uma versão da aplicação.
