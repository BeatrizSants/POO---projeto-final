from bottle import template,redirect, request
from app.controllers.datarecord import DataRecord
from app.controllers.score import Score

class Application():

    def __init__(self):
        self.pages = {
            'pagina':self.pagina,
            'portal': self.portal,
            'lobby': self.lobby,
            'jogo_marmota': self.jogo_marmota,
            'ranking': self.ranking
        }

        self.__model = DataRecord()
        self.__score = Score(self.__model)
        self.__current_username = None

    def render(self,page,username=None):
        content = self.pages.get(page)
        if not username:
            return content()
        else:
            return content(username)

    def get_session_id(self):
        return request.get_cookie('session_id')
    

    def is_authenticated(self, username):
        session_id = self.get_session_id()
        print(session_id)
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
    

    def create_user(self, username, password):
        if self.__model.user_exists(username):  #verifica se o usuário já existe
            return False  
        self.__model.book(username, password) #cria novo usuário
        return True 


    def logout_user(self):
        self.__current_username= None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

#delegando p/ classe Score p/ atualizar e carregar pontuacao
    def update_score(self, session_id, points):
        return self.__score.update_score(session_id, points)

    def get_score(self,session_id):
        return self.__score.get_score(session_id)


#-----------------------------------------------------------------------------------#



    def portal(self):
        return template('app/views/html/portal')
    
    def pagina(self,username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__model.getCurrentUser(session_id)
            return template('app/views/html/pagina', current_user=user, transfered = True)
        else:
            return template('app/views/html/pagina', current_user=None, transfered =False)


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
    
    
    def ranking(self):
        ranking_data = self.__score.get_ranking()
        return template('app/views/html/ranking', ranking=ranking_data, current_user=self.__current_username)
