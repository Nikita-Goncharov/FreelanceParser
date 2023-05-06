# import telebot
# bot = telebot.TeleBot("5519952596:AAFWojjQOn3gd2U5kwW1_y4nr_c9lVNqP54")
#
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     bot.send_message(message.from_user.id, message.text)
#

#
# def main():
#     print("Bot started....")
#     # bot.polling(none_stop=True, interval=0)

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters  # version - 13.3

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# TODO:
"""
1. Parser for freelance sites(BeautifulSoup)
2. Periodic tasks for parse sites(celery_periodic_tasks)
3. Send new offers(telegram) 
"""
chat_id: int = 983240870

updater = Updater("5519952596:AAFWojjQOn3gd2U5kwW1_y4nr_c9lVNqP54")
# updater.bot.sendMessage(chat_id='983240870', text='Hello there!')
dispatcher = updater.dispatcher


# TODO: WTF ???
# dispatcher.bot.send_message(chat_id=chat_id, text="Hello, world!!")
# dispatcher.bot.sendMessage(chat_id=chat_id, text="Hello, world!!")
#
# updater.bot.send_message(chat_id=chat_id, text="Hello, world!!")
# updater.bot.sendMessage(chat_id=chat_id, text="Hello, world!!")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, world!!")


def text(update, context):
    text = f'ECHO: {update.message.text} \n Message info: {update.message}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def caps(update, context):
    if context.args:
        text_caps = " ".join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No command args \n send: /caps [args1] [args..]")


start_handler = CommandHandler('start', start)
text_handler = MessageHandler(Filters.text & (~Filters.command), text)  # Если сообщение текстовое и не команда
caps_handler = CommandHandler('caps', caps)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(caps_handler)


if __name__ == "__main__":
    updater.start_polling()
    # updater.idle()  TODO: Нафига ?
