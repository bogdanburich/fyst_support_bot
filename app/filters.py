from telegram.ext import filters

SUPPORT_POSTFIX = '_fyst'

BASE_MESSAGE_FILTER = (~filters.COMMAND) & ~(filters.UpdateType.EDITED_MESSAGE)


class SupportFilter(filters.MessageFilter):
    def filter(self, message):
        username = message.from_user.username.lower()
        return username.endswith(SUPPORT_POSTFIX)
