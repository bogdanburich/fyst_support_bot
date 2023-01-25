from telegram.ext import filters

SUPPORT_POSTFIX = '_fyst'


class MessageFilter(filters.MessageFilter):
    def filter(self, message):
        return (
            not message.new_chat_members and not message.left_chat_member
        )


class SupportFilter(filters.MessageFilter):
    def filter(self, message):
        username = message.from_user.username.lower()
        return username.endswith(SUPPORT_POSTFIX)


BASE_MESSAGE_FILTERS = (~filters.COMMAND
                        & ~filters.UpdateType.EDITED_MESSAGE
                        & MessageFilter())
