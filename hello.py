import flask as fk
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField. SubmitField
from wtforms.validators import DataRequired

app = fk.Flask(__name__)
app.config['SECRET_KEY'] = 'Chave forte'

class Formulario(FlaskForm):
    nome = StringField("What is yout name?", validators=DataRequired)
    btnEnviar = SubmitField('Submit')


bootstrap = Bootstrap(app)
moment = Moment(app)

# Rota principal
@app.route('/', methods=['GET', 'POST'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      )
def index():

    form = Forumlario()
    nome = None

    if form.validate_on_submit():
        session['nome'] = form.name.data
        return reduirect(url_form('index'))
    
    return render_template('formulario.html', nome=session.get('nome'), form=form)

# Rota principal
@app.route('/atualizacao')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      )
def ultAtualizacao():

    return render_template('index.html', current_time=datetime.utcnow())


# Rota dinâmica
@app.route('/user/<name>/<prontuario>/<instituicao>')
def hello_user(name, prontuario, instituicao):

    return render_template('user.html', name=name, prontuario=prontuario, instituicao=instituicao)


# Contexto da requisição
@app.route('/contextorequisicao/<name>')
def requisicao_ctx(name):

    user_browser = fk.request.headers.get('User-Agent')
    user_IP = fk.request.headers.get('X-Forwarded-For')
    app_host = fk.request.headers.get('Host')

    return render_template(
            'contexto.html',
            name=name,
            user_browser=user_browser,
            user_IP=user_IP,
            app_host=app_host
        )


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

