from app.controllers.application import Application
from bottle import request, response, json_dumps

class GameService:
    def __init__(self):
        self.ctl = Application()  # Instância do controlador da aplicação
    
    def update_score(self):
        session_id = request.get_cookie('session_id')
        print(f"Session ID recebido: {session_id}")  # LOG

        if not session_id or not self.ctl.is_authenticated(self.ctl.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})

        data = request.json
        print(f"Dados recebidos: {data}")  # LOG

        points = data.get('score')
        if points is None:
            response.status = 400
            return json_dumps({"status": "error", "message": "Pontuação não fornecida."})

        result = self.ctl.update_score(session_id, points)
        print(f"Resultado da atualização: {result}")  # LOG
        response.content_type = "application/json"

        return result
        

    def get_score(self):
        session_id = request.get_cookie('session_id')
        if not session_id or not self.ctl.is_authenticated(self.ctl.get_authenticated_username(session_id)):
            response.status = 401
            return json_dumps({"status": "error", "message": "Usuário não autenticado."})
        
        result = self.ctl.get_score(session_id)
        return json_dumps(result)
