from bottle import request, response, json_dumps
#intermediario entre front e application, manipulacao de pontos
class GameService:
    def __init__(self, app):
        self.app = app
        self.accumulated_score = 0  # Variável que acumula os pontos

    def start_game(self):
        
        session_id = request.get_cookie('session_id')
        if not session_id:
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})
        
        username = self.app.get_authenticated_username(session_id)
        if not username:
            response.status = 401
            return json_dumps({"status": "error", "message": "Sessão inválida."})
        return json_dumps({"status": "success"})
        

    def add_score(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        new_score = self.app.update_score(session_id, 1)
        self.accumulated_score += 1
        
        print(self.accumulated_score)
        return json_dumps({"status": "success", "score": new_score})

    def take_score(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        current_score = self.accumulated_score
        print(f"Pontuação acumulada antes de subtrair: {current_score}")  # Log para depuração

        if current_score==0:
            new_score = self.app.update_score(session_id, -5)
        else:
            new_score = self.app.update_score(session_id, -current_score)
            self.accumulated_score = 0

        return json_dumps({
            "status": "success",
            "score": new_score,
            "accumulated_score": current_score
        })
        

    def end_game(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})
        self.accumulated_score = 0
        final_score = self.app.get_score(session_id)
        return json_dumps({"status": "success", "score": final_score})

    def get_score(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        score = self.accumulated_score
        return json_dumps({"score": score})
