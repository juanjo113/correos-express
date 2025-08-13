```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app as app


def send_email(to_email: str, subject: str, html: str):
    host = app.config['SMTP_HOST']
    port = app.config['SMTP_PORT']
    user = app.config['SMTP_USER']
    pwd = app.config['SMTP_PASS']
    use_tls = app.config['SMTP_USE_TLS']
    from_email = app.config['FROM_EMAIL']

    if not (host and port and user and pwd and from_email):
        app.logger.warning('SMTP no configurado; no se envía correo')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    with smtplib.SMTP(host, port) as server:
        if use_tls:
            server.starttls()
        server.login(user, pwd)
        server.sendmail(from_email, [to_email], msg.as_string())
    return True
```
