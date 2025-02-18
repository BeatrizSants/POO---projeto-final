from flask import Flask, render_template, request
import bcrypt

app = Flask(__name__)

# Para armazenar os usuários em memória (apenas para exemplo)
users_db = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form['username']
        password = request.form['password']

        # Verificar se o nome de usuário já existe
        if username in users_db:
            return "Usuário já existe!", 400  # Retorna um erro 400 se o usuário já existe

        # Gerando o salt e criptografando a senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Salvando o usuário com a senha criptografada
        users_db[username] = hashed_password

        return f"Usuário {username} registrado com sucesso!"

    except Exception as e:
        return str(e), 500  # Retorna um erro 500 se algo der errado

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        # Verificando se o usuário existe e se a senha está correta
        if username in users_db:
            # Verificando se a senha fornecida corresponde ao hash armazenado
            if bcrypt.checkpw(password.encode('utf-8'), users_db[username]):
                return "Login bem-sucedido!"
            else:
                return "Senha incorreta!", 401  # Retorna erro 401 se a senha estiver incorreta
        else:
            return "Usuário não encontrado!", 404  # Retorna erro 404 se o usuário não for encontrado

    except Exception as e:
        return str(e), 500  # Retorna erro 500 se houver uma falha no processo

if __name__ == '__main__':
    app.run(debug=True)