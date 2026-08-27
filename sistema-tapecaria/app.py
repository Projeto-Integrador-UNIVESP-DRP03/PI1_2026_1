import os

from app import create_app


app = create_app()

# para debug
#print(app.url_map)

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
    
# para abrir a aplicação sem o modo debug, use o comando abaixo    
##if __name__ == "__main__":
##    app.run(debug=False)