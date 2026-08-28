import os
import flask as fk
import wtforms as wf
import wtforms.validators as wtv

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = fk.Flask(__name__)
app.config['SECRET_KEY'] = 'they never gonna find out'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Tabelas BD
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# Chave Secreta
app.config['SECRET_KEY'] = 'Chave forte'

# Formularios Flask
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


class Cadastro(FlaskForm):
    nome = wf.StringField("Informe o seu nome:", validators=[wtv.DataRequired()])

    sobrenome = wf.StringField("Informe o seu sobrenome:", validators=[wtv.DataRequired()])

    instituicao = wf.StringField("Informe a sua Insituição de ensino:", validators=[wtv.DataRequired()])

    disciplina = wf.SelectField(
        "Informe a sua disciplina:",
        choices=[("DSWA5", "DSWA5"), ("DWBA4", "DWBA4"), ("Gestão de Projetos", "Gestão de Projetos")],
        validators=[wtv.DataRequired()]
    )

    enviar = wf.SubmitField('Submit')

class Main(FlaskForm):
    nome = wf.StringField('What is your name?', validators=[wtv.DataRequired()])

    enviar = wf.SubmitField('Submit')


# Rota Principal
@app.route('/', methods=['GET', 'POST'])
def index():

    main = Main()

    if main.validate_on_submit():
        user = User.query.filter_by(username=main.nome.data).first()

        if user is None:
            user = User(username=main.nome.data)
            db.session.add(user)
            db.session.commit()
            fk.session['nome'] = main.nome.data
            fk.session['known'] = False
            
        else:
            fk.session['nome'] = main.nome.data
            fk.session['known'] = True
            
        return fk.redirect(fk.url_for('index'))

    return fk.render_template('index.html', nome=fk.session.get('nome'), known=fk.session.get('known'), main=main)

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    cadastro = Cadastro()
    current_time = datetime.now(timezone.utc)
    user_IP = fk.request.headers.get('X-Forwarded-For')
    app_host = fk.request.headers.get('Host')

    if cadastro.validate_on_submit():
        nomeAntigo = fk.session.get('nome')
        if nomeAntigo is not None and nomeAntigo != cadastro.nome.data:
            fk.flash("Você alterou o seu nome!")

        fk.session['nome'] = cadastro.nome.data
        fk.session['sobrenome'] = cadastro.sobrenome.data
        fk.session['instituicao'] = cadastro.instituicao.data
        fk.session['disciplina'] = cadastro.disciplina.data

        return fk.redirect(fk.url_for('cadastrar'))

    return fk.render_template('cadastro.html',
                              current_time=current_time,
                              cadastro=cadastro,
                              nome=fk.session.get('nome'),
                              sobrenome=fk.session.get('sobrenome'),
                              instituicao=fk.session.get('instituicao'),
                              disciplina=fk.session.get('disciplina'),
                              app_host=app_host,
                              user_IP=user_IP
                              )

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



