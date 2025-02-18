from flask import Flask
from app.route import init_routes

app = Flask(__name__)

# Inicializa as rotas do app
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)