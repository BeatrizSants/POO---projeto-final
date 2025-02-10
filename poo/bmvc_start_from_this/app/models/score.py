class Score:
    def __init__(self, username, score):
        self.username = username
        self.score = score
        self.session_id = None  # Opcional: se precisar associar ao session_id

    def save(self, db):
        """Salva a pontuação do usuário no banco de dados."""
        db.add_score(self)

    def __repr__(self):
        return f"Score(username={self.username}, score={self.score})"
