import flask as fk
import wtforms as wf
import wtforms.validators as wtv

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime, timezone

# Inicialização
app = fk.Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Chave Secreta
app.config['SECRET_KEY'] = 'Chave forte'

# Formulario Flask
class Formulario(FlaskForm):
    nome = wf.StringField("What is yout name?", validators=[wtv.DataRequired()])
    enviar = wf.SubmitField('Submit')

class Login(FlaskForm):
    usuario = wf.StringField('', validators=[wtv.DataRequired()], 
                             render_kw={"placeholder": "Usuário ou e-mail"}
                            )
    senha = wf.PasswordField('', validators=[wtv.DataRequired()], 
                             render_kw={"placeholder": "Informe a sua senha"}
                            )
    enviar = wf.SubmitField('Enviar')


# Rota principal
@app.route('/')
def index():

    return fk.render_template('index.html', current_time=datetime.now(timezone.utc))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    login = Login()
    current_time = datetime.now(timezone.utc)

    if login.validate_on_submit():
        fk.session['usuario'] = login.usuario.data

        return fk.redirect('/loginResponse')
    
    return fk.render_template('login.html', login=login, current_time=current_time)

# Retorno do login
@app.route('/loginResponse')
def loginResponse():

    usuario = fk.session.get('usuario')
    current_time = datetime.now(timezone.utc)

    return fk.render_template('loginResponse.html', current_time=current_time, usuario=usuario)

# Formulário
@app.route('/formulario', methods=['GET', 'POST'])
def forms():

    form = Formulario()
    nome = None

    if form.validate_on_submit():
        nomeAntigo = fk.session.get('nome')
        if nomeAntigo is not None and nomeAntigo != form.nome.data:
            fk.flash('Looks like you have changed your name!')
        fk.session['nome'] = form.nome.data
        return fk.redirect(fk.url_for('forms'))
    
    return fk.render_template('formulario.html', nome=fk.session.get('nome'), form=form)


# Rota dinâmica
@app.route('/user/<name>/<prontuario>/<instituicao>')
def hello_user(name, prontuario, instituicao):

    return fk.render_template('user.html', name=name, prontuario=prontuario, instituicao=instituicao)


# Contexto da requisição
@app.route('/contextorequisicao/<name>')
def requisicao_ctx(name):

    user_browser = fk.request.headers.get('User-Agent')
    user_IP = fk.request.headers.get('X-Forwarded-For')
    app_host = fk.request.headers.get('Host')

    return fk.render_template(
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



