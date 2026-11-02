import wtforms as wf
import wtforms.validators as wfv
from flask_wtf import FlaskForm

# Formularios Flask
class Formulario(FlaskForm):
    nome = wf.StringField("What is yout name?", validators=[wfv.DataRequired()])
    enviar = wf.SubmitField('Submit')

class Login(FlaskForm):
    usuario = wf.StringField('', validators=[wfv.DataRequired()],
                             render_kw={"placeholder": "Usuário ou e-mail"}
                            )
    senha = wf.PasswordField('', validators=[wfv.DataRequired()],
                             render_kw={"placeholder": "Informe a sua senha"}
                            )
    enviar = wf.SubmitField('Enviar')

class Cadastro(FlaskForm):
    nome = wf.StringField("Informe o seu nome:", validators=[wfv.DataRequired()])

    sobrenome = wf.StringField("Informe o seu sobrenome:", validators=[wfv.DataRequired()])

    instituicao = wf.StringField("Informe a sua Insituição de ensino:", validators=[wfv.DataRequired()])

    disciplina = wf.SelectField(
        "Informe a sua disciplina:",
        choices=[("DSWA5", "DSWA5"), ("DWBA4", "DWBA4"), ("Gestão de Projetos", "Gestão de Projetos")],
        validators=[wfv.DataRequired()]
    )

    enviar = wf.SubmitField('Submit')

class Main(FlaskForm):
    nome = wf.StringField('Qual é o seu nome?', validators=[wfv.DataRequired()], render_kw={"placeholder": "Escreva seu nome aqui"})

    email = wf.StringField('Qual é o seu email (Envio de notificação do novo usuário)?', validators=[wfv.DataRequired()], render_kw={"placeholder": "Escreva seu e-mail aqui"})

    '''
    opcaoEmail = wf.BooleanField('Deseja enviar e-mail para flaskaulasweb@zohomail.com?')

        funcao = wf.SelectField(
        "Qual é a sua função (Role)?",
        choices=[('Administrator', 'Administrator'), ('Moderator', 'Moderator'), ('User', 'User')],
        validators=[wfv.DataRequired()])
    '''

    enviar = wf.SubmitField('Enviar')

class Editar_Usuario(FlaskForm):
    username = wf.StringField(validators=[wfv.DataRequired(), wfv.Length(max=64)])
