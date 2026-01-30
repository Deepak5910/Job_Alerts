import csv
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def send_emmail():
    df = pd.read_csv("data/job_master.csv")
    html_table = df.to_html(
    index=False,
    border=1,
    justify="left"
    )
    html_body = f"""
<html>
<head>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            font-family: Arial, sans-serif;
        }}
        th, td {{
            border: 1px solid #dddddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <p>Hello,</p>
    <p>Please find below the latest job opportunities:</p>
    {html_table}
    <p>Regards,<br>Job Alert Bot</p>
</body>
</html>
    """

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText


    sender_email = os.getenv("sender_email")
    receiver_email = os.getenv("receiver_email")
    app_password = os.getenv("app_password")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Job Alerts"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


