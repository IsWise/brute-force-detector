
# Brute Force Detector

This script monitors SSH logs for failed login attempts and provides various security features to detect brute-force attacks. It is designed to analyze logs, detect suspicious behavior, and notify users through various channels such as email, Slack, and logging systems. Additionally, it includes geolocation functionality to trace the IP addresses of potential attackers.

## Features

- **SSH Log Analysis**: Monitors and analyzes SSH logs for failed login attempts.
- **Geolocation**: Provides the geolocation of suspicious IP addresses.
- **Email Alerts**: Sends email notifications when suspicious activity is detected.
- **Slack Alerts**: Notifies a Slack channel when a brute-force attempt is detected.
- **Custom Logging**: Allows custom log reporting to file.
- **ElasticSearch Integration**: Optional integration with Elasticsearch for advanced data storage and searching.
- **Dual License**: Available under MIT or GPL-3.0 license.

## Requirements

To run this script, you need to have the following dependencies installed:

- Python 3.x
- Install the required dependencies:
  ```
  pip install requests geocoder python-dotenv smtplib elasticsearch
  ```

## Configuration

1. **Environment Variables**: 
   You need to configure your environment variables for email, Slack, and other necessary credentials. Create a `.env` file in the same directory as the script with the following content:
   ```
   EMAIL_HOST='smtp.your_email_provider.com'
   EMAIL_PORT=587
   EMAIL_USER='your_email@example.com'
   EMAIL_PASS='your_email_password'

   SLACK_WEBHOOK_URL='https://hooks.slack.com/services/your/webhook/url'

   # Elasticsearch configuration (optional)
   ES_HOST='localhost'
   ES_PORT=9200
   ```

2. **SSH Log File**:
   - Ensure you have access to the SSH log file (e.g., `/var/log/auth.log` on Linux).
   - You can modify the script to specify the path to your log file.

## Usage

1. **Running the Script**:
   After configuring the environment variables and log path, you can run the script with the following command:
   ```
   python brute_force_detector.py
   ```
   This will start the log analysis and send notifications if brute-force attempts are detected.

2. **Logs and Reports**:
   - The script will generate logs based on the analyzed SSH log file.
   - Reports can be customized to be written to a local file.
   - The detected IP addresses of brute-force attempts will be printed and stored in the report file.

## License

This project is Educational Use License.

## Acknowledgments

- This script was created by **iswise**.
- The following libraries were used:
  - `requests`: For handling HTTP requests.
  - `geocoder`: For obtaining geolocation data for IP addresses.
  - `python-dotenv`: For managing environment variables.
  - `smtplib`: For sending email notifications.
  - `elasticsearch`: For optional integration with Elasticsearch for storage and analysis.
