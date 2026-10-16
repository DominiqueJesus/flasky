from . import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.JSON, nullable=False, default=list)
    destinatario = db.Column(db.JSON, nullable=False, default=list)
    assunto = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.String(500), nullable=False)
    dataHora = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc).replace(microsecond=0))

    def __repr__(self):
        return (
            f'<DE: {self.remetente!r} PARA: {self.destinatario!r} '
            f'ASSUNTO: {self.assunto!r} ENVIADO EM: {self.dataHora!r}>'
        )