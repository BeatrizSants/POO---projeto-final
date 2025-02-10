from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response

app = Bottle()
ctl = Application() #


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')

@app.route('/', method='GET')
def login():
    session_id = ctl.get_session_id()
    username = ctl.get_authenticated_username(session_id)
    if session_id:
        username = ctl.get_authenticated_username(session_id)
        if username:  # Se o usuário estiver autenticado
            return redirect(f'/lobby/{username}')
    return ctl.render('portal') 

@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return ctl.render('/')
    else:
        return ctl.render('pagina',username)


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
    
@app.route('/lobby/<username>', method='GET')
def lobby(username):
    if ctl.is_authenticated(username):
        return ctl.render('lobby', username)
    else:
        return redirect('/')

    
@app.route('/logout', method='POST')
def logout():
      ctl.logout_user()
      response.delete_cookie('session_id')
      return redirect('/')
#-----------------------------------------------------------------------------
# Suas rotas aqui:



#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)
