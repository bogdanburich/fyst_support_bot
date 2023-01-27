from telegram import Update
from telegram.ext import ContextTypes


def set_locale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get('locale'):
        title = update.message.chat.title
        if title.lower().endswith('ru'):
            context.chat_data['locale'] = 'ru'
            return
        context.chat_data['locale'] = 'en'
        return


async def get_jobs(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    return context.application.job_queue.get_jobs_by_name(str(chat_id))
