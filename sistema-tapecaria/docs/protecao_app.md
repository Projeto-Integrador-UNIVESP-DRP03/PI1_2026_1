## Proteção da aplicação

A aplicação usa sessões Flask para autenticação e mensagens temporárias. Todas as rotas administrativas exigem login.

Flask precisa de uma chave secreta (secret_key) para gerenciar sessões e cookies de forma segura. Sem ela, qualquer tentativa de usar session gera:

```text
RuntimeError: The session is unavailable because no secret key was set.
```

### Boas práticas
Não use uma string simples como chave em produção.  

Gere uma chave aleatória e segura. Você pode usar o módulo secrets do Python:

```python
import secrets
  app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(32))
```


O código acima deve estar no arquivo  '\_\_init__.py'. 

secrets.token_hex(32) → gera uma chave aleatória de 64 caracteres hexadecimais, forte o suficiente para produção, caso a variável não esteja definida.


No terminal você precisa iniciar a senha:
```shell
setx SECRET_KEY "a_chave_escolhida"
```
E irá aparecer:
```bash
ÊXITO: o valor especificado foi salvo.
```
### Configuração do acesso administrativo

O usuário e o hash da senha são fornecidos por variáveis de ambiente. Nunca grave a senha em arquivos do projeto.

Gere um hash uma única vez no ambiente virtual:

```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('SUA_SENHA'))"
```

Configure os valores no Windows:

```powershell
setx ADMIN_USERNAME "admin"
setx ADMIN_PASSWORD_HASH "HASH_GERADO"
setx SECRET_KEY "UMA_CHAVE_LONGA_E_ALEATORIA"
```

Depois de configurar as variáveis, abra um novo terminal e execute a aplicação. O logout é feito por uma requisição POST protegida por CSRF.


