import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_email(to_email, subject, html_content):
    """
    Envía un correo usando SendGrid API.

    :param to_email: Dirección de correo del destinatario
    :param subject: Asunto del correo
    :param html_content: Contenido HTML del correo
    """
    try:
        message = Mail(
            from_email=current_app.config["MAIL_DEFAULT_SENDER"],
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
        response = sg.send(message)
        return response.status_code, response.body, response.headers
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        return 500, None, None  # Retorna un error 500 en caso de fallo
