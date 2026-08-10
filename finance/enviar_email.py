import smtplib
import random
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import time

load_dotenv()

def enviar_email(email, username):
    corpo_email = f"""
                    <p>Seja muito bem-vindo, <b>{username}</b>!</p>

                    <p>Fico muito feliz por você estar testando meu projeto.</p>

                    <p>Qualquer dúvida sobre a aplicação, fique à vontade para me chamar por aqui:</p>
                    <ul>
                        <li>GitHub: <a href="https://github.com/Felipe0132">github.com/Felipe0132</a></li>
                        <li>LinkedIn: <a href="https://linkedin.com/in/felipe-silva-64026b358">linkedin.com/in/felipe-silva-64026b358</a></li>
                        <li>E-mail: felipesiilvaa2006@gmail.com@gmail.com</li>
                    </ul>

                    <p>Também deixo aqui o convite para conhecer alguns dos meus outros projetos no GitHub!</p>

                    <p>Abraço,<br>Felipe Silva!</p>
                    """
    
    msg = MIMEText(corpo_email, "html")
    msg["Subject"] = "Codigo para cadastrar em Finatech"
    msg["From"] = "finatech013@gmail.com"
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 587) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)