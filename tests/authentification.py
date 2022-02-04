"""
Test authentification to an API with OAuth2

python tests/authentification.py
"""
import os
import requests
from dotenv import load_dotenv

HOST = "http://127.0.0.1:8002"


# Save username in a file .env
load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Prepare form to send in POST
root = f"http://{host}:{port}"
parameters = {
    "username": username,
    "password": password,
}
headers = {"content-type": "application/x-www-form-urlencoded"}

# Validate and get token
response = requests.post(f"{root}/token", data=parameters, headers=headers).json()
print(response["access_token"])
