import logging
import sys

import i18n
from config import BASE_DIR, BOT_TOKEN, MESSAGE_DELAY, TICKET_MIN_LENGTH
from filters import BASE_MESSAGE_FILTERS, SupportFilter
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler)
from utils import get_jobs, set_locale

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def create_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add ticket to bitrix
    set_locale(update, context)
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    locale = context.chat_data.get('locale')
    if not context.args:
        text = i18n.t('ticket_no_args', locale=locale)
        await context.bot.send_message(chat_id=chat_id, text=text,
                                       reply_to_message_id=message_id)
        return

    ticket_name = ' '.join(context.args)
    if len(ticket_name) < TICKET_MIN_LENGTH:
        text = i18n.t('ticket_too_short', locale=locale)
        await context.bot.send_message(chat_id=chat_id, text=text,
                                       reply_to_message_id=message_id)
        return

    text = i18n.t('ticket_created', locale=locale, ticket_name=ticket_name)
    await context.bot.send_message(chat_id=chat_id, text=text,
                                   reply_to_message_id=message_id)
    context.chat_data['message_sent'] = False


async def request_in_process(context: ContextTypes.DEFAULT_TYPE):
    locale = context.chat_data.get('locale')
    text = i18n.t('wait_message', locale=locale)
    message_id = context.chat_data.get('message_id')
    context.chat_data['message_sent'] = True
    await context.bot.send_message(chat_id=context.job.chat_id, text=text,
                                   reply_to_message_id=message_id)


async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_locale(update, context)
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    context.chat_data['message_id'] = update.message.message_id
    if not jobs and not context.chat_data.get('message_sent'):
        context.job_queue.run_once(request_in_process, MESSAGE_DELAY,
                                   chat_id=chat_id, name=str(chat_id))


async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    context.chat_data['message_sent'] = False
    if jobs:
        for job in jobs:
            job.schedule_removal()


def check_creds() -> bool:
    return all([
        BOT_TOKEN
    ])


def main():
    if not check_creds():
        sys.exit()

    i18n.load_path.append(BASE_DIR + '/locales')
    i18n.set('filename_format', '{locale}.{format}')

    application = Application.builder().token(BOT_TOKEN).build()

    message_handler = MessageHandler(~SupportFilter()
                                     & BASE_MESSAGE_FILTERS,
                                     user_message)
    support_message_handler = MessageHandler(SupportFilter()
                                             & BASE_MESSAGE_FILTERS,
                                             support_message)
    ticket_handler = CommandHandler('ticket', create_ticket)

    application.add_handler(message_handler)
    application.add_handler(support_message_handler)
    application.add_handler(ticket_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
