import wtforms as wf
import wtforms.validators as wfv
from flask_wtf import FlaskForm

# Formularios Flask
class CadastrarProfessor(FlaskForm):
    nome = wf.StringField(
        'Cadastre o novo Professor:', 
        validators=[wfv.DataRequired()]
    )
    
    disciplina = wf.SelectField(
        "Disciplina associada:",
        choices=[("DSWA5", "DSWA5"), ("GPSA5", "GPSA5"), ("IHCA5", "IHCA5"), ("SODA5", "SODA5"), ("PJIA5", "PJIA5"), ("TCOA5", "TCOA5")],
        validators=[wfv.DataRequired()]
    )

    enviar = wf.SubmitField('Cadastrar')
