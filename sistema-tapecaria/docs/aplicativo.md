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
├── static
|   ├── css
|   |   └── estilo.css
|   └── imagens [Repositório de imagens]
|          ├── Catalogos
|          └── Identidade_visual [Aqui está o arquivo .ico]
|
├── desktop.py
|
├── venv 
|
└── requirements.txt 
```


O ponto de entrada do executável é `desktop.py`. Ele inicia o Waitress e abre o navegador automaticamente.

## 2. Instalar dependências

No ambiente virtual, na pasta `sistema-tapeçaria`:

```bash
pip install -r requirements.txt
```
| Dica: Use Python 3.10 ou 3.11 para evitar problemas de compatibilidade com PyInstaller.

## 3. Gere o executável

Ainda na pasta `sistema-tapeçaria`, execute:

```bash
pyinstaller --noconfirm ZitOS.spec
```

#### Explicação dos parâmetros:
- `ZitOS.spec` → usa a configuração versionada do executável.
- O arquivo gerado utiliza `desktop.py`, templates, arquivos estáticos e banco inicial.

## 4. Resultado

Após rodar o comando:

O PyInstaller cria as pastas `build/` e `dist/`.

Dentro de `dist/ZitOS/` estará o arquivo `ZitOS.exe`.

Esse é o arquivo que você pode enviar para qualquer pessoa. Basta dar dois cliques e a aplicação abrirá no navegador.

## 5. Distribuição

Envie a pasta ``dist/ZitOS/`` completa ou compacte essa pasta.

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

Consulte o `requirements.txt` do projeto; ele já inclui Waitress, ReportLab, Pillow e PyInstaller.

Antes de distribuir, configure `SECRET_KEY`, `ADMIN_USERNAME` e `ADMIN_PASSWORD_HASH` no ambiente da máquina.

