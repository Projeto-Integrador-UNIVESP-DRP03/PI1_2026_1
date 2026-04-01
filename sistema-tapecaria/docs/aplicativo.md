# Guia: Criando um Executável Portátil (.exe) para Aplicação Flask

Este documento explica como transformar uma aplicação Flask em um arquivo `.exe` que pode ser executado em qualquer computador Windows, mesmo sem Python instalado.

---

## 1. Preparar o Projeto

Estrutura recomendada:
# Estrutura de pastas do Sistema
```
sistema-tapecaria
│
(...)
├── statics
|   ├── css
|   |   └── estilo.css
|   └── imagens [Repositório de imagens]
|          ├── Catalogos
|          └── Identidade_visual [Aqui está o arquivo .ico]
|
├── app.py
|
├── venv 
|
└── requirements.txt 
```


No final do `app.py`, adicione:
```python
import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)
```

Isso garante que o navegador abra automaticamente quando o programa iniciar.

## 2. Instalar dependências

No ambiente virtual, na pasta `sistema-tapeçaria`:

```bash
pip install -r requirements.txt
pip install pyinstaller
```
| Dica: Use Python 3.10 ou 3.11 para evitar problemas de compatibilidade com PyInstaller.

## 3. Gere o executável

Ainda na pasta `sistema-tapeçaria`, execute:

```bash
pyinstaller --onefile --noconsole --icon=static\imagens\Identidade_visual\logo_icone.ico --name=ZitOS app.py
```

#### Explicação dos parâmetros:
- `--onefile` → gera um único arquivo `.exe`.

- `--noconsole` → oculta a janela preta do terminal.

- `icon=caminho/nome_logo.ico` → define o ícone da aplicação.

- `name=ZitOS` → nome do executável final.

- `app.py` → arquivo principal da aplicação.

## 4. Resultado

Após rodar o comando:

O PyInstaller cria as pastas `build/` e `dist/`.

Dentro de `dist/` estará o arquivo `ZitOS.exe`.

Esse é o arquivo que você pode enviar para qualquer pessoa. Basta dar dois cliques e a aplicação abrirá no navegador.

## 5. Distribuição

Envie apenas o arquivo ``.exe`` (ou compacte a pasta ``dist/``).

O usuário final não precisa instalar Python.

Ao executar, o navegador abrirá automaticamente em ``http://127.0.0.1:5000``.

## 6. Complementos

Se ocorrer erro com DLLs (_ctypes), reinstale Python em versão estável (3.10/3.11) e recrie o ambiente virtual.

Para facilitar, você pode usar a ferramenta gráfica:

````bash
pip install auto-py-to-exe
auto-py-to-exe
````
Ela abre uma interface para configurar tudo sem precisar lembrar dos parâmetros.

Se precisar recriar o aplicativo (.exe), recomenda-se deletar as pastas `build/` e `dist/` e o arquivo `<nome_app>.spec`.

## 7. Requirements.txt
Exemplo mínimo para Flask + SQLAlchemy:

````
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.48
````

Para gerar o .exe, inclua também:

````
pyinstaller==6.3.0
auto-py-to-exe==2.42.0
````

