from gevent import monkey
monkey.patch_all()
from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response, json_dumps
from app.models.gameservice import GameService
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json

app = Bottle()
ctl = Application()
gameservice = GameService(ctl)
#relação de associação gamesevice e application

# Rotas:
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/ws_login', method='GET')
def ws_login():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return

    try:
        message = ws.receive()
        if message == 'login_success':
            ws.send(json.dumps({'status': 'success', 'message': 'Login bem-sucedido!'}))
        else:
            ws.send(json.dumps({'status': 'error', 'message': 'Login inválido!'}))
    except WebSocketError as e:
        print(f"Erro WebSocket: {e}")
    finally:
        ws.close()

@app.route('/ws_signup', method='GET')
def ws_signup():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return

    try:
        message = ws.receive()
        if message == 'signup_success':
            ws.send(json.dumps({'status': 'success', 'message': 'Cadastro bem-sucedido!'}))
        else:
            ws.send(json.dumps({'status': 'error', 'message': 'Cadastro inválido!'}))
    except WebSocketError as e:
        print(f"Erro WebSocket: {e}")
    finally:
        ws.close()

@app.route('/', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        return redirect(f'/lobby/{username}')
    else:
        return template('app/views/html/portal', error="Nome de usuário ou senha inválidos!")

@app.route('/signup', method='POST')
def signup():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not ctl.create_user(username, password):
        return template('app/views/html/portal', error="Nome de usuário já existe!")

    ws = request.environ.get('wsgi.websocket')
    if ws:
        try:
            ws.send(json.dumps({'status': 'success', 'message': 'Cadastro bem-sucedido!'}))
        except WebSocketError as e:
            print(f"Erro WebSocket: {e}")

    return redirect('/')

@app.route('/lobby/<username>', method='GET')
def lobby(username):
    if not username or not ctl.is_authenticated(username):
        return redirect('/')
    return ctl.render('lobby', username)

@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return ctl.render('/')
    else:
        return ctl.render('pagina', username)

@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    return redirect('/')

@app.route('/jogo_marmota/<username>', method='GET')
def jogo_marmota(username):
    if ctl.is_authenticated(username):
        return ctl.render('jogo_marmota', username)
    else:
        return redirect('/')

@app.route('/ranking/<username>', method='GET')
def ranking(username):
    if not username or not ctl.is_authenticated(username):
        return redirect('/')
    return ctl.ranking()

@app.route('/start_game', method='POST')
def start_game():
    return gameservice.start_game()

@app.route('/add_score', method='POST')
def add_score():
    return gameservice.add_score()

@app.route('/take_score', method='POST')
def take_score():
    return gameservice.take_score()

@app.route('/end_game', method='POST')
def end_game():
    return gameservice.end_game()

@app.route('/get_score', method='GET')
def get_score():
    return gameservice.get_score()

def start_servers():
    http_server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    print("Servidor rodando em: http://0.0.0.0:8080")
    http_server.serve_forever()

if __name__ == '__main__':
    start_servers()



    