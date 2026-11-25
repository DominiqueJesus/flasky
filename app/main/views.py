from datetime import datetime
from zoneinfo import ZoneInfo

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from . import main
from .. import db
from ..models import Professor
from .forms import CadastrarProfessor


def hora_local():
    return datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")


@main.route("/", methods=["GET"])
def index():
    modulo = request.args.get("modulo", "").strip()
    modulos_validos = {"alunos", "cursos", "disciplinas", "ocorrencias"}
    if modulo not in modulos_validos:
        modulo = ""
    return render_template(
        "index.html",
        nome="SEU NOME",
        prontuario="SEU PRONTUÁRIO",
        modulo=modulo,
        current_time=hora_local(),
    )


@main.route("/professores", methods=["GET", "POST"])
def cadastrar_professor():
    cadastro_professor_form = CadastrarProfessor()
    if cadastro_professor_form.validate_on_submit():
        nome = cadastro_professor_form.nome.data.strip()
        disciplina = cadastro_professor_form.disciplina.data
        professor = Professor(nome=nome, disciplina=disciplina)
        db.session.add(professor)
        try:
            db.session.commit()
            flash("Professor cadastrado com sucesso!")
        except IntegrityError:
            db.session.rollback()
            flash("Já existe um professor cadastrado com esse nome.")
        return redirect(url_for("main.cadastrar_professor"))

    professores = Professor.query.order_by(Professor.nome.asc()).all()
    return render_template(
        "cadastro_professores.html",
        cadastro_professor_form=cadastro_professor_form,
        professores=professores,
        current_time=hora_local(),
    )

# Rota: Alunos
@main.route('/alunos')
def cadastrar_aluno():

    return render_template('nao_disponivel.html')

# Rota: Cursos
@main.route('/cursos', methods=['GET', 'POST'])
def cadastrar_curso():

    return render_template('nao_disponivel.html')

# Rota: Disciplinas
@main.route('/disciplinas', methods=['GET', 'POST'])
def cadastrar_disciplina():

    return render_template('nao_disponivel.html')

# Rota: Ocorrências
@main.route('/ocorrencias', methods=['GET', 'POST'])
def cadastrar_ocorrencia():

    return render_template('nao_disponivel.html')

