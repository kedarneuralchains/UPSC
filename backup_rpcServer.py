import subprocess
import smtplib
import os
import requests
import tarfile
import time
from datetime import datetime, timedelta
from email.message import EmailMessage

def stop_coind():
    subprocess.run(["/usr/local/bin/coin-cli", "stop"]) # safely stop the coin daemon
    time.sleep(10)

def create_backup():
    backup_dir = "/home/ubuntu/.data_directory" # set the coin data directory like .bitcoin
    backup_dest = "/home/ubuntu/backups" # set the backup destination path
    os.makedirs(f"{backup_dest}/latest", exist_ok=True)
    os.makedirs(f"{backup_dest}/historic", exist_ok=True)

    # Create backup in latest directory
    with tarfile.open(f"{backup_dest}/latest/backup.tar.gz", "w:gz") as tar:
        tar.add(backup_dir, arcname=".")
    latest_backup = "backup.tar.gz"

    # Create backup with timestamp
    date_time = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    with tarfile.open(f"{backup_dest}/historic/backup_{date_time}.tar.gz", "w:gz") as tar:
        tar.add(backup_dir, arcname=".")
    historic_backup = f"backup_{date_time}.tar.gz"

    # Remove backups older than 10 days
    for file in os.listdir(f"{backup_dest}/historic"):
        file_path = os.path.join(f"{backup_dest}/historic", file)
        if os.path.getmtime(file_path) < (datetime.now() - timedelta(days=10)).timestamp():
            os.remove(file_path)
    
    return latest_backup, historic_backup

def start_coind():
    subprocess.run(["/usr/local/bin/coind"]) # start back the coin daemon once backup is created

def send_email(subject, latest_backup, historic_backup):
    body = f"Half-hourly backup of the data directory has been created:\n\nLatest Backup: {latest_backup}\nHistoric Backup: {historic_backup}"
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'send@email.com' # sender email, the one you'll use with SMTP
    msg['To'] = 'receiver@email.com' # receiver email address

    with smtplib.SMTP('smtp.url.com', 123) as server: # set SMTP URL and Port
        server.login('send@email.com', 'password123') # set smtp email and respective password
        server.send_message(msg)
        
# this one compares local and explorer block height and sends notification if local node is behind
def compare_block_height():
    local_blockheight = subprocess.run(["coin-cli", "getblockcount"], capture_output=True, text=True).stdout.strip()
    response = requests.get('https://explorer.coin.com/api/getblockcount')
    remote_blockheight = response.json()

    if abs(int(remote_blockheight) - int(local_blockheight)) >= 3:
        send_email("Blockheight Alert", f"Local daemon blockheight is behind. Local: {local_blockheight}, Remote: {remote_blockheight}")

# Main execution
stop_coind()
latest_backup, historic_backup = create_backup()
start_coind()
send_email("Coin RPC Node Backup Notification", latest_backup, historic_backup)
compare_block_height()