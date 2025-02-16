from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response, json_dumps

app = Bottle()
ctl = Application() #


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.route('/', method='GET')
def login():
    return ctl.render('portal') 


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username= ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, \
        secure=True, max_age=3600)
        return redirect(f'/lobby/{username}')
    else:
        return redirect('/')
    

@app.route('/signup', method='POST')
def signup():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not ctl.create_user(username, password): return template('app/views/html/portal', error="Nome de usuário já existe!")
    return redirect('/')  # Redireciona para login após o cadastro

    
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
        return ctl.render('pagina',username)

    
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



    #pontuação jogo
@app.post('/update_score')
def update_score():
    session_id = request.get_cookie('session_id')

    if not session_id or not ctl.is_authenticated(ctl.get_authenticated_username(session_id)):
        response.status = 401
        return json_dumps({"status": "error", "message": "Usuário não autenticado."})

    data = request.json

    points = data.get('score')
    if points is None:
        response.status = 400
        return json_dumps({"status": "error", "message": "Pontuação não fornecida."})

    result = ctl.update_score(session_id, points)
    response.content_type = "application/json"

    if isinstance(result, tuple):
        response.status = 400
        return json_dumps(result[0])
    return json_dumps(result)


@app.route('/get_score', method='GET')
def get_score():
    result = ctl.get_score()
    return json_dumps(result)





#-----------------------------------------------------------------------------
# Suas rotas aqui:



#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)
