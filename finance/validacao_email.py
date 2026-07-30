import smtplib
import random
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import time

load_dotenv()

tokens = {}

def gerar_token(email_cadastro):
    token = random.randint(100000, 999999)
    tokens[email_cadastro] = (token, time.time())
    return tokens

def enviar_email(email_cadastrado, chave):
    msg = MIMEText(f"Seu codigo de verificação é: {chave[email_cadastrado][0]}") # Mensagem dentro do email
    msg["Subject"] = "Codigo para cadastrar em Finatech"
    msg["From"] = "finatech013@gmail.com"
    msg["To"] = email_cadastrado

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)

def enviar_codigo(email_cadastrado):
    token = gerar_token(email_cadastrado)
    enviar_email(email_cadastrado, token)

def validar_codigo(email_cadastrado, token_digitado):
    if email_cadastrado not in tokens:
        return False

    token, time_inicio = tokens[email_cadastrado]

    if time.time() - time_inicio > 600: # Passou 10 min
            del tokens[email_cadastrado]
            return False
    
    if int(token_digitado) == token:
        del tokens[email_cadastrado]
        return True

    return False