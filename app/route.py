from flask import render_template, jsonify
from app.application import QuizGame

quiz = QuizGame()  # Criamos uma instância do jogo

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/get_questions")
    def get_questions():
        return jsonify(quiz.get_questions())