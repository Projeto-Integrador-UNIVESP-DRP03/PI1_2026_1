# Seeds do Banco de Dados

## O que são Seeds

**Seeds** são scripts utilizados para **inserir dados iniciais em um banco de dados**.
Eles são muito usados durante o desenvolvimento de sistemas para:

* Popular tabelas com **dados de teste**
* Inserir **dados padrão do sistema**
* Facilitar **testes e demonstrações da aplicação**

Ao invés de inserir dados manualmente no banco, o desenvolvedor executa um script que cria automaticamente os registros necessários.

---

## Como os Seeds foram utilizados neste projeto

Neste sistema de gerenciamento para tapeçaria automotiva, os seeds foram utilizados para inserir **dados iniciais de catálogo**, que serão utilizados durante a criação de orçamentos e pedidos.

Foram populadas as seguintes tabelas:

* **Tecido**
* **Espuma**
* **Costura**
* **Cor**

Essas tabelas funcionam como **catálogos de opções disponíveis no sistema**, permitindo que o usuário selecione materiais e características ao registrar um serviço.

Exemplos de dados inseridos:

* Tipos de tecido (Courvin, Couro Natural, Suede)
* Cores dos materiais (Preto, Cinza, Bege, Vermelho)
* Tipos de espuma (D28, D33, D45)
* Tipos de costura (Simples, Dupla, Diamante)

---

## Arquivo de Seeds do Projeto

Os dados foram inseridos através do arquivo:

```
database/seeds_catalogos.py
```

Esse arquivo utiliza o **SQLAlchemy**, a mesma biblioteca usada pelo sistema para manipular o banco de dados.

O script cria objetos das classes do modelo e os adiciona à sessão do banco:

```python
db.session.add_all(tecidos)
db.session.add_all(espumas)
db.session.add_all(costuras)
db.session.add_all(cores)
db.session.commit()
```

---

## Como executar os Seeds

Antes de inserir os dados, o banco precisa estar criado. Portanto, a ordem correta é:

1. **Recriar o banco de dados**

```
python database/init_db.py
```

2. **Executar o script de seeds**

```
python database/seeds_catalogos.py
```

Após a execução, as tabelas de catálogo já estarão populadas com dados iniciais.

---

## Importância no desenvolvimento

O uso de seeds traz várias vantagens para o desenvolvimento do sistema:

* Padroniza os dados iniciais do projeto
* Facilita testes e demonstrações
* Evita inserção manual de dados
* Permite recriar rapidamente o ambiente de desenvolvimento

Por esses motivos, o uso de seeds é uma prática comum em projetos que utilizam bancos de dados relacionais.
