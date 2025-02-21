from app.models.user_account import UserAccount
import json
import uuid
import bcrypt
import base64
import logging

logging.basicConfig(level=logging.DEBUG)
class DataRecord():
    def __init__(self):
        self.__user_accounts= [] # banco (json)
        self.__authenticated_users = {}
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__user_accounts = []


    def book(self,username,password):
        new_user= UserAccount(username,password,score=0)
        self.__user_accounts.append(new_user)
        self.save_to_json()

    def save_to_json(self):
        user_data = []
        for user_account in self.__user_accounts:
            user_dict = vars(user_account)
            
            if isinstance(user_account.password, bytes):
                # Se a senha já for bytes (hash bcrypt), simplesmente a armazena
                user_dict['password'] = user_account.password.decode('utf-8')
            else:
                # Caso contrário, cria o hash e armazena diretamente o valor do hash bcrypt
                if not self._is_hashed(user_account.password):
                    hashed_password = bcrypt.hashpw(user_account.password.encode('utf-8'), bcrypt.gensalt())
                    user_dict['password'] = hashed_password.decode('utf-8')

            user_data.append(user_dict)

        # Grava os dados no arquivo JSON
        with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
            json.dump(user_data, arquivo_json, indent=4)

    def _is_hashed(self, password):
    # Check if the password looks like a bcrypt hash
        return password.startswith('$2a$') or password.startswith('$2b$')

        

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
        return None 

    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username:
                logging.debug(f"Senha armazenada (bcrypt): {user.password}")
                
                # Decodifica a senha armazenada (bcrypt)
                try:
                    stored_hashed_password = user.password.encode('utf-8')
                    logging.debug(f"Senha recuperada (bytes): {stored_hashed_password}")
                except Exception as e:
                    logging.error(f"Erro ao processar a senha: {e}")
                    return None

                # Verifica se a senha fornecida corresponde ao hash armazenado
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                    logging.debug(f"Stored hash: {stored_hashed_password}")
                    # Se a senha corresponder, cria uma nova sessão para o usuário
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    return session_id  # Retorna o ID da sessão

        return None



    def user_exists(self, username):
        return any(user.username == username for user in self.__user_accounts) #se usuário já existe


    def logout(self, session_id):
        if session_id and session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] #remove o usuário logado

    def update_score(self, session_id, points): #atualiza pontuacão do usuário
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
        #todos os usuários com suas pontuações
        return [vars(user) for user in self.__user_accounts]