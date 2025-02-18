import json

class Question:
    """ Representa uma única pergunta do quiz """
    def __init__(self, pergunta, opcoes, resposta):
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.resposta = resposta

    def to_dict(self):
        """ Retorna a pergunta em formato de dicionário (JSON compatível) """
        return {
            "pergunta": self.pergunta,
            "opcoes": self.opcoes,
            "resposta": self.resposta
        }

class QuizGame:
    """ Gerencia o jogo de perguntas """
    def __init__(self, db_path="app/database.json"):
        self.db_path = db_path
        self.questions = self.load_questions()

    def load_questions(self):
        """ Carrega as perguntas do banco de dados JSON """
        with open(self.db_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Question(**q) for q in data]

    def get_questions(self):
        """ Retorna todas as perguntas em formato JSON """
        return [q.to_dict() for q in self.questions]