import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

MESSAGES = {
    'wait': 'We\'ve got your request, please wait for a while',
    'ticket': 'The ticket has been created successfully'
}

MESSAGE_DELAY = 5
