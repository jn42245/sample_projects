# Created by Thierry Tran
# Created on 5 January 2023
# Script to automatically send email

import json
import smtplib
import ssl
import logging
from email.message import EmailMessage


def load_json(path: str, mode: str):
    with open(path, mode) as f:
        x = json.load(f)
    return x


def read_cred(credentials: str):
    keys = ['address',
            'app_password',
            'password']
    with open(credentials, "r") as f:
        local_cred = json.load(f)
    if not all(key in keys for key in local_cred.keys()):
        raise Exception("Bad config file")
    return [local_cred['address'], local_cred['app_password'], local_cred['password']]


def send_email(sender: str, receiver: str, password: str, subject: str, body: str, port: int):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info('Connecting to Gmail.')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, em.as_string())
    logging.info('Email sent.')
    return None


if __name__ == '__main__':
    import os

    wk_dir = os.path.dirname(os.path.abspath("__file__"))
    cred_path = load_json(os.path.join(wk_dir, 'data', 'email_cred_path.json'), "r")

    subject = "Subject Test"
    body = "XXXXXXXXXX"

    send_email(read_cred(cred_path)[0], "xxx@xxx", read_cred(cred_path)[1], subject, body, 465)

