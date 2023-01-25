from telegram.ext.filters import MessageFilter

SUPPORT_POSTFIX = '_fyst'


class SupportFilter(MessageFilter):
    def filter(self, message):
        username = message.from_user.username.lower()
        return username.endswith(SUPPORT_POSTFIX)
