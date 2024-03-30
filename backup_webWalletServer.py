import subprocess
import smtplib
import os
import requests
from datetime import datetime, timedelta
from email.message import EmailMessage

def create_mysql_backup():
    # Database configuration
    DB_HOST = "127.0.0.1" # set your db URL
    DB_PORT = "1234" # set your db port
    DB_DATABASE = "db_name" # set your db name
    DB_USERNAME = "db_user" # set your db username
    DB_PASSWORD = "db_password" # set your db password
    backup_dest = "/home/ubuntu/backups" # set your backup path
    os.makedirs(f"{backup_dest}/latest", exist_ok=True) 
    os.makedirs(f"{backup_dest}/historic", exist_ok=True)

    # Create backup file names
    date_time = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    latest_backup = f"{backup_dest}/latest/mysql_backup.sql" # latest backup is saved here, replacing last one.
    historic_backup = f"{backup_dest}/historic/mysql_backup_{date_time}.sql" # historic backups are collected in this directory

    # Command to execute
    dump_cmd = f"mysqldump -h {DB_HOST} -P {DB_PORT} -u {DB_USERNAME} -p{DB_PASSWORD} {DB_DATABASE} > {latest_backup}"
    subprocess.run(dump_cmd, shell=True, check=True)
    subprocess.run(f"cp {latest_backup} {historic_backup}", shell=True)

    # Remove backups older than 10 days
    for file in os.listdir(f"{backup_dest}/historic"):
        file_path = os.path.join(f"{backup_dest}/historic", file)
        if os.path.getmtime(file_path) < (datetime.now() - timedelta(days=10)).timestamp():
            os.remove(file_path)

    return latest_backup, historic_backup


def send_email(subject, latest_backup, historic_backup):
    # Extract just the file names
    latest_backup_file = os.path.basename(latest_backup)
    historic_backup_file = os.path.basename(historic_backup)

    body = f"Quarter-hourly backup of the DB has been created:\n\nLatest Backup: {latest_backup_file}\nHistoric Backup: {historic_backup_file}"
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'send@email.com' # sender email, the one you'll use with SMTP
    msg['To'] = 'receiver@email.com' # receiver email address

    with smtplib.SMTP('smtp.url.com', 123) as server: # set SMTP URL and Port
        server.login('send@email.com', 'password123') # set smtp email and respective password
        server.send_message(msg)

# Main execution
latest_backup, historic_backup = create_mysql_backup()
send_email("MySQL Database Backup Notification", latest_backup, historic_backup)