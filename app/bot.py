import os
import logging
from telegram import Update

from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from filters import SupportFilter, BASE_MESSAGE_FILTER
from config import MESSAGES, MESSAGE_DELAY, TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def create_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add bitrix client
    chat_id = update.message.chat_id
    text = MESSAGES['ticket']
    await context.bot.send_message(chat_id=chat_id, text=text)
    return

async def get_jobs(chat_id: int, context: ContextTypes.DEFAULT_TYPE): 
    return context.application.job_queue.get_jobs_by_name(str(chat_id))

async def request_in_process(context: ContextTypes.DEFAULT_TYPE):
    text = MESSAGES['wait']
    message_id = context.chat_data.get('message_id')
    await context.bot.send_message(chat_id=context.job.chat_id, text=text, reply_to_message_id=message_id)

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    context.chat_data['message_id'] = update.message.message_id
    if not jobs:
        context.job_queue.run_once(request_in_process, MESSAGE_DELAY, chat_id=chat_id, name=str(chat_id))
    return

async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    jobs = await get_jobs(chat_id, context)
    if jobs:
        for job in jobs:
            job.schedule_removal()
    return
 

if __name__ == '__main__':
    
    application = Application.builder().token(TOKEN).build()

    message_handler = MessageHandler(~SupportFilter() & BASE_MESSAGE_FILTER, user_message)
    support_message_handler = MessageHandler(SupportFilter() & BASE_MESSAGE_FILTER, support_message)
    ticket_handler = CommandHandler('ticket', create_ticket)


    application.add_handler(message_handler)
    application.add_handler(support_message_handler)
    application.add_handler(ticket_handler)

    application.run_polling()
