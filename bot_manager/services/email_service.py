import aiosmtplib
from datetime import datetime
from aiosmtplib.typing import SMTPStatus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bot_manager.settings import settings, timezone


class EmailService:
    @staticmethod
    async def send_registration_email(email_to: str, password: str):
        text = f"""<div>Уважаемый пользователь!</div>
                    <div>Вы были зарегистрированы в системе ""{settings.project_name}"".</div>
                    <ul>Данные для входа:
                        <li>Логин: {email_to}</li>
                        <li>Пароль: {password}</li>
                    </ul>"""
        subject = f'Создана учетная запись в системе {settings.project_name}.'
        await EmailService.send_email(email_to, subject=subject, body=text)

    @staticmethod
    async def send_email(email_to: str, subject: str, body: str, plain_body: str = None):
        message = MIMEMultipart("alternative")
        message['From'] = settings.email_sender
        message['To'] = email_to
        message['Subject'] = subject
        message['Date'] = datetime.now(tz=timezone).strftime('%d.%m.%Y %H:%M:%S')
        plain_text_message = MIMEText(plain_body or body, "plain", "utf-8")
        html_message = MIMEText(body, "html", "utf-8")
        message.attach(plain_text_message)
        message.attach(html_message)
        smtp_client = aiosmtplib.SMTP(hostname=settings.email_server, use_tls=True)
        async with smtp_client:
            await smtp_client.ehlo()
            response = await smtp_client.auth_login(settings.email_account, settings.email_password)
            if response.code != SMTPStatus.auth_successful:
                raise Exception('SMTP authentication connection error')

            if settings.debug_mode:
                await smtp_client.send_message(message, recipients=settings.email_test_recipient)
            else:
                await smtp_client.send_message(message)
