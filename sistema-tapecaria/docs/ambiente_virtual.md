# Ambiente Virtual

## 🐍 Ambiente Virtual (Python)

Um **ambiente virtual** é um espaço isolado dentro do projeto onde ficam instaladas as bibliotecas Python necessárias para a aplicação.
Isso evita conflitos entre dependências de diferentes projetos e garante que todos os membros da equipe utilizem **as mesmas versões de bibliotecas**.

No repositório, **não compartilhamos o ambiente virtual**, apenas a lista de dependências (`requirements.txt`), permitindo que cada desenvolvedor recrie o ambiente localmente.

---

## 📋 Pré-requisitos

Antes de iniciar, é necessário ter instalado:

* Python 3.10 ou superior
* pip (gerenciador de pacotes do Python)
* Git

---

# ⚙️ Configuração do Ambiente

## 1️⃣ Criar o ambiente virtual

Dentro da pasta do projeto, execute:

```bash
python -m venv venv
```

caso dê algum erro, execute o seguinte comando uma única vez
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Isso criará uma pasta chamada:

```
venv/
```

Essa pasta contém todas as bibliotecas e executáveis do ambiente virtual.

---

## 2️⃣ Ativar o ambiente virtual

### Windows

```bash
venv\Scripts\activate.ps1
```
Quando o ambiente estiver ativo, o terminal mostrará algo como:

```
(venv)
```

---

## 3️⃣ Instalar dependências do projeto

Para instalar todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

---

# 📦 Gerenciamento de Dependências

## Adicionar uma nova biblioteca

1. Instale a biblioteca desejada:

```bash
pip install nome-da-biblioteca
```

2. Atualize o arquivo de dependências:

```bash
pip freeze > requirements.txt
```

3. Faça commit da atualização:

```bash
git add requirements.txt
git commit -m "adiciona nova dependência"
git push
```

---

## Atualizar dependências após alterações no repositório

Sempre que o projeto for atualizado:

```bash
git pull
pip install -r requirements.txt
```

Isso garante que todas as dependências estejam sincronizadas.

---

# ⚠️ Boas práticas

* ❌ **Nunca subir a pasta `venv/` para o repositório**
* ✔️ Sempre atualizar o `requirements.txt` ao instalar novas bibliotecas
* ✔️ Manter as versões das bibliotecas registradas
* ✔️ Ativar o ambiente virtual antes de executar o projeto