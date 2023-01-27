import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = str(Path(__file__).resolve().parent)

BOT_TOKEN = os.getenv('BOT_TOKEN')

MESSAGE_DELAY = 30

TICKET_MIN_LENGTH = 10
