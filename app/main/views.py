from datetime import datetime, timezone
import flask as fk
from . import main
from .. import db
from .forms import Formulario, Login, Cadastro, Main
from ..models.User import User
from ..models.Role import Role
from ..models.Email import Email, send_mail
from sqlalchemy import func

# CAMINHOS DO SITE

# Rota Principal
@main.route('/', methods=['GET', 'POST'])
def index():

    main = Main()

    if main.validate_on_submit():
        user = User.query.filter_by(username=main.nome.data).first()
        #role_name = main.funcao.data
        role = Role.query.filter_by(name="User").first()

        '''if role is None:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.commit()'''

        if user is None:
            user = User(username=main.nome.data, role=role)
            app_config = fk.current_app.config

            '''if main.opcaoEmail.data is True:'''
            recipients = [
                            address
                                for address in (
                                    app_config.get('FLASKY_ADMIN'),
                                    app_config.get('MAIL_RECIPIENT')
                                )
                                if address
            ]
            
            '''else:
                recipients = app_config.get('FLASKY_ADMIN')'''
            
            send_mail(main.nome.data, recipients)

            db.session.add(user)
            db.session.commit()
            fk.session['nome'] = main.nome.data
            fk.session['known'] = False

        else:
            fk.session['nome'] = main.nome.data
            fk.session['known'] = True

        return fk.redirect(fk.url_for('index'))

    users = User.query.all()
    #roles = Role.query.all()
    users_count = db.session.query(func.count(User.id)).scalar()
    #roles_count = db.session.query(func.count(Role.id)).scalar()

    return fk.render_template('index.html',
                              nome=fk.session.get('nome'),
                              known=fk.session.get('known'),
                              main=main,
                              users=users,
                              #roles=roles,
                              users_count=users_count,
                              #roles_count=roles_count
                              )

#Emails enviados
@main.route('/emailsEnviados')
def listarEmails():

    emails = Email.query.order_by(Email.dataHora.desc()).all()

    return fk.render_template('emailsEnviados.html', emails=emails)

# Cadastro
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    cadastro = Cadastro()
    current_time = datetime.now(timezone.utc)
    user_IP = fk.request.headers.get('X-Forwarded-For')
    main_host = fk.request.headers.get('Host')

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
                              main_host=main_host,
                              user_IP=user_IP
                              )

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():

    login = Login()
    current_time = datetime.now(timezone.utc)

    if login.validate_on_submit():
        fk.session['usuario'] = login.usuario.data

        return fk.redirect('/loginResponse')

    return fk.render_template('login.html', login=login, current_time=current_time)

# Retorno do login
@main.route('/loginResponse')
def loginResponse():

    usuario = fk.session.get('usuario')
    current_time = datetime.now(timezone.utc)

    return fk.render_template('loginResponse.html', current_time=current_time, usuario=usuario)

# Formulário
@main.route('/formulario', methods=['GET', 'POST'])
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
@main.route('/user/<name>/<prontuario>/<instituicao>')
def hello_user(name, prontuario, instituicao):

    return fk.render_template('user.html', name=name, prontuario=prontuario, instituicao=instituicao)

# Contexto da requisição
@main.route('/contextorequisicao/<name>')
def requisicao_ctx(name):

    user_browser = fk.request.headers.get('User-Agent')
    user_IP = fk.request.headers.get('X-Forwarded-For')
    main_host = fk.request.headers.get('Host')

    return fk.render_template(
            'contexto.html',
            name=name,
            user_browser=user_browser,
            user_IP=user_IP,
            main_host=main_host
        )

# Código de status do servidor
@main.route('/codigostatusdiferente')
def requisicao_indevida():

    return '<p>Bad request</p>', 400

# Criar objeto de resposta
@main.route('/objetoresposta')
def obj_resposta():

    myobj = fk.make_response("<h1>This document carries a cookie!</h1>")

    myobj.set_cookie('answer', '42')

    return myobj

# Redirecionar para outro site
@main.route('/redirecionamento')
def redirecionar():

    return fk.redirect('https://ptb.ifsp.edu.br/')

# Abortar função de view
@main.route('/abortar')
def abortar_site():

    return fk.abort(404)