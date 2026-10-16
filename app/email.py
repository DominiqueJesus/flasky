from . import db
from .models import Email
from html import escape
from flask import current_app
import requests

# Enviar E-mail
def send_mail(username, recipients):

    api_url = current_app.config.get('API_URL')
    api_key = current_app.config.get('API_KEY')
    api_from = current_app.config.get('API_FROM')
    if not all((api_url, api_key, api_from)):
        raise RuntimeError('Configure API_URL, API_KEY e API_FROM para enviar e-mails.')

    safe_username = escape(username)
    destinatarios = recipients if isinstance(recipients, list) else [recipients]
    assunto = "Novo usuário adicionado ao Flasky!"
    admin_name = current_app.config.get('FLASKY_ADMIN_NAME') or 'Administrador'
    admin_id = current_app.config.get('FLASKY_ADMIN_ID') or ''
    texto = (
        f"Olá, {admin_name} ({admin_id})! "
        f"Foi adicionado um novo usuário ao site Flasky, com o username {safe_username}"
    )

    response = requests.post(
        api_url,
        auth=("api", api_key),
        data={
            "from": api_from,
            "to": destinatarios,
            "subject": assunto,
            "text": texto,
            "html": f"""
                <html>
                    <body>
                        <h2>Novo usuário adicionado ao Flasky!</h2>
                        <p>Olá, <strong>{escape(admin_name)}</strong>!</p>
                        <p>Um novo usuário foi adicionado ao site Flasky, com o username <strong>{safe_username}</strong>.</p>
                        <h3>Dados do aluno:</h3>
                        <ul>
                            <li>Prontuário: {escape(admin_id)}</li>
                            <li>Nome completo: {escape(admin_name)}</li>
                        </ul>
                    </body>
                </html>
            """
        }
    )
    response.raise_for_status()

    email = Email(
        remetente=safe_username if isinstance(safe_username, list) else [safe_username,],
        destinatario=destinatarios,
        assunto=assunto,
        texto=texto
    )
    db.session.add(email)
    db.session.commit()

    return response