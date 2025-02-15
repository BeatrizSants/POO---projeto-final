from bottle import template,redirect, request
from app.controllers.datarecord import DataRecord


class Application():

    def __init__(self):
        self.pages = {
            'pagina':self.pagina,
            'portal': self.portal,
            'lobby': self.lobby,
            'jogo_marmota': self.jogo_marmota
        }

        self.__model = DataRecord()
        self.__current_username = None # Criando a instância da classe WebSocketHandler

    def render(self,page,username=None):
        content = self.pages.get(page, self.helper)
        if not username:
            return content()
        else:
            return content(username)

    def get_session_id(self):
        return request.get_cookie('session_id')
    
    def helper(self):
        return template('app/views/html/helper')
    
    def portal(self):
        return template('app/views/html/portal')
    
    def pagina(self,username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__model.getCurrentUser(session_id)
            return template('app/views/html/pagina', current_user=user, transfered = True)
        else:
            return template('app/views/html/pagina', current_user=None, transfered =False)


    def is_authenticated(self, username):
        session_id = self.get_session_id()
        current_username = self.__model.getUserName(session_id)
        return username == current_username


    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self.__current_username= self.__model.getUserName(session_id)
            return session_id, username
        return None, None
    def get_authenticated_username(self, session_id):
        return self.__model.getUserName(session_id)
    
    def logout_user(self):
        self.__current_username= None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)
    def lobby(self, username=None):
        if self.is_authenticated(username):
            user = self.__model.getCurrentUser(self.get_session_id())
            return template('app/views/html/lobby', current_user=user)
        else:
            return redirect('/')
        
    def jogo_marmota(self, username=None):
        if self.is_authenticated(username):
            user = self.__model.getCurrentUser(self.get_session_id())
            return template('app/views/html/jogo_marmota', current_user=user)
        else:
            return redirect('/')
    
    def update_score(self, session_id, points):
        if self.__model.update_score(session_id, points):
            return {"status":"success", "message": "Pontuação atualizada"}
        else:
            return {"status":"error", "message": "Falha ao atualizar pontuação"}
        
    def get_score(self):
        session_id = self.get_session_id()
        if session_id:
            return self.__model.get_score(session_id)
        return {"status": "error", "message": "Sessão não encontrada"}
