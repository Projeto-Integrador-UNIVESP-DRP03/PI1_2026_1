## Proteção da aplicação

Esta proteção é necessária para gerar alertas na tela. Como o alerta na pesquisa de CPF/CNPJ.

Flask precisa de uma chave secreta (secret_key) para gerenciar sessões e cookies de forma segura. Sem ela, qualquer tentativa de usar session gera:

```bach
RuntimeError: The session is unavailable because no secret key was set.
```

### Boas práticas
Não use uma string simples como chave em produção.  

Gere uma chave aleatória e segura. Você pode usar o módulo secrets do Python:

```python
import secrets
a linha de código
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
### Atenção, essa senha não precisa ser usada em mais nenhum outro lugar.


