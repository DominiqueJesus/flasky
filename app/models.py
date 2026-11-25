from . import db


class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, nullable=False, index=True)
    disciplina = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Professor {self.nome!r}>"
