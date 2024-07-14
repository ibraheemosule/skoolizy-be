import os
from flask import jsonify
import schedule
import time
from datetime import datetime
import threading
import re

from utils.custom_error import CustomError

email_schedules = {}


def schedule_email(id, subject, message, recipient, interval, event_start_date):
    job = schedule.every(int(interval)).days.do(lambda: send_email(subject, message, recipient))
    email_schedules[id] = job

    def run_schedule():
        while datetime.now() <= datetime.strptime(event_start_date, '%Y-%m-%d'):
            schedule.run_pending()
            time.sleep(1)

    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.start()


def stop_scheduled_email(job_id):
    if job_id in email_schedules:
        schedule.cancel_job(email_schedules[job_id])
        del email_schedules[job_id]
    else:
        raise CustomError(f"No reminder found with id: {job_id}", 404)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, message, recipients):
    from_email = os.getenv('FLASK_EMAIL')
    password = os.getenv("FLASK_EMAIL_PASSWORD")

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, password)

        for recipient in recipients:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = recipient

            html_part = MIMEText(message, 'html')
            msg.attach(html_part)

            server.sendmail(from_email, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")


def is_email_valid(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None
