import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

MESSAGES = {
    'wait': 'We\'ve got your request, please wait for a while',
    'ticket': 'The ticket has been created successfully'
}

ERRORS = {
    'ticket_no_args': 'Please, specify the ticket name, for example: /ticket My ticket',
    'ticket_too_short': 'The ticket name must be at least 10 characters long'
}

MESSAGE_DELAY = 5

TICKET_MIN_LENGTH = 10
