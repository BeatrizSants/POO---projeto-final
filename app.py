from gevent import monkey
monkey.patch_all()

from bottle import Bottle, route, run, request, response, static_file, template, redirect, abort, TEMPLATE_PATH
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import bcrypt
import json

# Configura o Bottle para procurar templates na pasta "templates"
TEMPLATE_PATH.append("./templates")

app = Bottle()

# Simulação de banco de dados em memória
users = {}

# Função para criptografar a senha
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Função para verificar a senha
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Rota para servir arquivos estáticos (CSS)
@app.route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')

# Rota para a página de login
@app.route('/')
def login():
    return template('login')

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return template('cadastro')

# Rota para WebSocket
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            if message:
                data = json.loads(message)
                if data['type'] == 'login':
                    # Processar login via WebSocket
                    username = data['username']
                    password = data['password']
                    if username in users and check_password(password, users[username]):
                        wsock.send(json.dumps({'success': True, 'message': 'Login bem-sucedido!'}))
                    else:
                        wsock.send(json.dumps({'success': False, 'message': 'Usuário ou senha incorretos!'}))

                elif data['type'] == 'cadastro':
                    # Processar cadastro via WebSocket
                    username = data['username']
                    password = data['password']
                    if username in users:
                        wsock.send(json.dumps({'success': False, 'message': 'Usuário já existe!'}))
                    else:
                        users[username] = hash_password(password)
                        wsock.send(json.dumps({'success': True, 'message': 'Cadastro bem-sucedido!'}))

        except WebSocketError:
            break

# Iniciar o servidor
if __name__ == '__main__':
    run(app, host='localhost', port=8080, server='gevent', handler_class=WebSocketHandler)