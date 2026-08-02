import flask as fk

app = fk.Flask(__name__)

# Rota principal

@app.route('/')
def index():

    text1 = '<h1>Hello World!</h1>'
    text2 = '<h2>Disciplina PTBDSWS</h2>'

    return text1 + text2


# Rota dinâmica

@app.route('/user/<name>')
def hello_user(name):
    return f'<h1>Hello, {name}!</h1>'


# Contexto da requisição

@app.route('/contextorequisicao')
def requisicao_ctx():

    user_browser = fk.request.headers.get('User-Agent')

    return f'Your browser is {user_browser}'


# Código de status do servidor

@app.route('/codigostatusdiferente')
def requisicao_indevida():

    return '<p>Bad request</p>', 400


# Criar objeto de resposta

@app.route('/objetoresposta')
def obj_resposta():

    myobj = fk.make_response("<h1>This document carries a cookie!</h1>")

    myobj.set_cookie('answer', '42')

    return myobj


# Redirecionar para outro site

@app.route('/redirecionamento')
def redirecionar():

    return fk.redirect('https://ptb.ifsp.edu.br/')


# Abortar função de view

@app.route('/abortar')
def abortar_site():

    return fk.abort(404)

