import logging

from config import ERRORS, MESSAGE_DELAY, MESSAGES, TICKET_MIN_LENGTH, TOKEN
from filters import BASE_MESSAGE_FILTERS, SupportFilter
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def create_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add ticket to bitrix
    chat_id = update.message.chat_id
    if not context.args:
        text = ERRORS['ticket_no_args']
        await context.bot.send_message(chat_id=chat_id, text=text)
        return
    ticket_name = ' '.join(context.args)
    if len(ticket_name) < TICKET_MIN_LENGTH:
        text = ERRORS['ticket_too_short']
        await context.bot.send_message(chat_id=chat_id, text=text)
        return
    text = MESSAGES['ticket']
    await context.bot.send_message(chat_id=chat_id,
                                   text=f'{text}: {ticket_name}')
    return


async def get_jobs(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    return context.application.job_queue.get_jobs_by_name(str(chat_id))


async def request_in_process(context: ContextTypes.DEFAULT_TYPE):
    text = MESSAGES['wait']
    message_id = context.chat_data.get('message_id')
    context.chat_data['message_sent'] = True
    await context.bot.send_message(chat_id=context.job.chat_id, text=text,
                                   reply_to_message_id=message_id)


async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    context.chat_data['message_id'] = update.message.message_id
    if not jobs and not context.chat_data.get('message_sent'):
        context.job_queue.run_once(request_in_process, MESSAGE_DELAY,
                                   chat_id=chat_id, name=str(chat_id))
    return


async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    context.chat_data['message_sent'] = False
    if jobs:
        for job in jobs:
            job.schedule_removal()
    return


if __name__ == '__main__':

    application = Application.builder().token(TOKEN).build()

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
