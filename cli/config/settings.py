"""
CLI Config Settings
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Host and base URL
HOST = os.getenv("HOST", "http://127.0.0.1:8002")
BASE_URL = f"{HOST}/v1"

# Default limit and timeout in seconds
LIMIT = int(os.getenv("LIMIT", "40"))
TIMEOUT = int(os.getenv("LIMIT", "12"))

# Username and password
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
