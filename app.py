from flask import Flask, render_template, jsonify
import os
import json
import random

class JogoLogica:
    def __init__(self, arquivo_perguntas):
        self.pontuacao = 0
        self.pergunta_atual = None
        self.perguntas = self.carregar_perguntas(arquivo_perguntas)

    def carregar_perguntas(self, arquivo_perguntas):
        """Carrega as perguntas do JSON, verificando se o arquivo existe."""
        if not os.path.exists(arquivo_perguntas):
            print(f"Erro: Arquivo {arquivo_perguntas} não encontrado.")
            return []  # Retorna uma lista vazia para evitar erro

        with open(arquivo_perguntas, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Erro ao carregar JSON.")
                return []

app = Flask(__name__)
jogo = JogoLogica("perguntas.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_pergunta")
def get_pergunta():
    if not jogo.perguntas:
        return jsonify({"erro": "Nenhuma pergunta disponível"})
    
    pergunta = random.choice(jogo.perguntas)  # Escolhe uma pergunta aleatória
    return jsonify(pergunta)

if __name__ == "__main__":
    app.run(debug=True)