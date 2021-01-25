import time
from actions import send_action, ChatAction
from logging import getLogger
from security import getUserByID


@send_action(ChatAction.TYPING)
def any_msg_handler(bot, update, user_data):
    logger = getLogger("simple_msg")
    user_id = update.message.from_user.id
    user = getUserByID(user_id)
    chat_id = update.message.chat_id
    logger.info("{}\n{}\n".format(user, update.message))
    time.sleep(0.5)
    bot.send_message(chat_id=chat_id, text="Hasta la vista, baby.")
