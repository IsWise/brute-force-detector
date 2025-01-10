# Script developed by: iswise
# License: Educational Use License
# For ethical and educational use only. Do not use without authorization.

import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import geocoder
from collections import Counter
from dotenv import load_dotenv
import requests
from elasticsearch import Elasticsearch
import time

# Load environment variables
load_dotenv()

# Define the path for logs and other variables
LOG_PATH = input("Enter the path to the SSH log file: ")

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
GEOLocator = geocoder.get_geocoder_for_provider("ipinfo")
MAX_FAILED_ATTEMPTS = 10  # Threshold for sending alerts
GEOCACHE_LIFETIME = 3600  # 1 hour cache expiry

# Global cache to store geolocation data
geolocation_cache = {}

def send_email_alert(subject, body, to_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            text = msg.as_string()
            server.sendmail(EMAIL_USER, to_email, text)
            print("Email alert sent successfully.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"Unexpected error sending email: {e}")

def send_slack_alert(message):
    if SLACK_TOKEN:
        try:
            response = requests.post('https://slack.com/api/chat.postMessage',
                                     headers={'Authorization': f'Bearer {SLACK_TOKEN}'},
                                     data={'channel': '#alerts', 'text': message})
            if response.status_code == 200 and response.json().get('ok'):
                print("Slack alert sent successfully.")
            else:
                print(f"Slack API Error: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending Slack alert: {e}")
    else:
        print("Slack Token is not configured properly.")

def get_geolocation(ip):
    # First check if IP is in cache
    if ip in geolocation_cache:
        return geolocation_cache[ip]

    try:
        location = geolocator.geocode(ip)
        if location:
            geolocation_cache[ip] = location
            return location
    except Exception as e:
        print(f"Error fetching geolocation for {ip}: {e}")
        return None

    return None

def analyze_logs(log_path):
    try:
        if not os.path.exists(log_path):
            print(f"Log file {log_path} not found.")
            return

        with open(log_path, 'r') as file:
            logs = file.readlines()

        if not logs:
            print("Log file is empty.")
            return

        failed_attempts = []
        ip_pattern = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"

        for line in logs:
            match = re.search(ip_pattern, line)
            if match:
                failed_attempts.append(match.group(1))

        ip_counts = Counter(failed_attempts)

        print("\nBrute Force Attempts Report (by: iswise):")
        print("-" * 50)
        for ip, attempts in ip_counts.items():
            print(f"IP: {ip} - Failed Attempts: {attempts}")
            if attempts >= MAX_FAILED_ATTEMPTS:
                print(f"Alert: IP {ip} exceeded max failed attempts.")
                send_alert(ip, attempts)

        with open("iswise_brute_force_report.txt", "w") as report:
            report.write("Brute Force Attempts Report (by: iswise):\n")
            report.write("-" * 50 + "\n")
            for ip, attempts in ip_counts.items():
                report.write(f"IP: {ip} - Failed Attempts: {attempts}\n")

        print("\nReport saved to 'iswise_brute_force_report.txt'")

    except FileNotFoundError:
        print(f"The specified log file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_alert(ip, failed_attempts):
    location = get_geolocation(ip)
    if location:
        message = f"Alert! Suspicious activity detected from IP {ip}. {failed_attempts} failed login attempts."
        message += f"\nLocation: {location.address if location else 'Unknown'}"
    else:
        message = f"Alert! Suspicious activity detected from IP {ip}. {failed_attempts} failed login attempts."
    
    send_email_alert("Brute Force Attempt Alert", message, EMAIL_USER)
    send_slack_alert(message)

def clean_geolocation_cache():
    """Periodically clean the cache to avoid memory overflow."""
    global geolocation_cache
    if len(geolocation_cache) > 1000:
        geolocation_cache.clear()
        print("Geolocation cache cleared due to size limit.")

if __name__ == "__main__":
    # Run the log analysis periodically
    while True:
        analyze_logs(LOG_PATH)
        clean_geolocation_cache()
        time.sleep(600)  # Delay between runs (10 minutes)
