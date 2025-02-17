from bottle import request, response, json_dumps

class GameService:
    def __init__(self, app):
        self.app = app  # Application já foi instanciado em route.py

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

    def hit_mole(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        new_score = self.app.update_score(session_id, 1)
        return json_dumps({"status": "success", "score": new_score})

    def hit_trap(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        new_score = self.app.update_score(session_id, -1)
        return json_dumps({"status": "success", "score": new_score})

    def end_game(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        final_score = self.app.get_score(session_id)
        return json_dumps({"status": "success", "score": final_score})

    def get_score(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.app.is_authenticated(self.app.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        score = self.app.get_score(session_id)
        return json_dumps({"score": score})
