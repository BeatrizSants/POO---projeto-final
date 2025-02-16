from app.models.user_account import UserAccount
import json
import uuid

class DataRecord():
    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):
        self.__user_accounts= [] # banco (json)
        self.__authenticated_users = {}
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101','101010'))


    def book(self,username,password):
        new_user= UserAccount(username,password,score=0)
        self.__user_accounts.append(new_user)
        self.save_to_json()

    def save_to_json(self):
        with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
            user_data = [vars(user_account) for user_account in \
            self.__user_accounts]
            json.dump(user_data, arquivo_json, indent=4)


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getUserName(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None
    def getUserSessionId(self, username):
        for session_id in self.__authenticated_users:
            if username == self.__authenticated_users[session_id].username:
                return session_id
        return None  # Retorna None se o usuário não for encontrado


    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None

    def user_exists(self, username):
        return any(user.username == username for user in self.__user_accounts)


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado

    def update_score(self, session_id, points):
        user = self.getCurrentUser(session_id)
        if user:
            user.score += points
            self.save_to_json()
            return True
        return False

    def get_score(self, session_id):
        user = self.getCurrentUser(session_id)
        if user:
            return user.score
        return 0

    def get_all_users(self):
        # Retorna todos os usuários com suas pontuações
        return [vars(user) for user in self.__user_accounts]