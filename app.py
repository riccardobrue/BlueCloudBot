import requests
import urllib
from urllib.request import urlopen
from telegram.ext import (Updater, MessageHandler, Filters)


# ==============================================================================================
# Receives a file from the chat
# ==============================================================================================
def send_file(bot, update):
    userInfo = update.message.from_user

    user_first_name = userInfo.first_name
    user_id = userInfo.id

    print("==================================")
    print("User First Name: " + user_first_name)
    print("User ID: " + str(user_id))
    print("==================================")

    item=None
    file_name=None
    file_type=None
    file_size=None

    if(update.message.document is not None):
        item=update.message.document
        file_name = item.file_name
        file_type = item.mime_type
        file_size = item.file_size
    elif(update.message.audio is not None):
        item=update.message.audio
        file_name = item.file_id
        file_type = item.mime_type
        a, b = file_type.split("/")
        file_name=file_name+"."+b
        file_size = item.file_size
    elif(update.message.video is not None):
        item=update.message.video
        file_name = item.file_id
        file_type = item.mime_type
        a, b = file_type.split("/")
        file_name=file_name+"."+b
        file_size = item.file_size
    elif(update.message.voice is not None):
        item=update.message.voice
        file_name = item.file_id
        file_type = item.mime_type
        a, b = file_type.split("/")
        file_name=file_name+"."+b
        file_size = item.file_size
    elif(update.message.photo is not None):
        update.message.reply_text("You must send images as a file!")
        return

    print("_File name:")
    print(file_name)
    print("_File type:")
    print(file_type)
    print("_File size:")
    print(file_size)

    if(file_size>20000000):
        update.message.reply_text("File too big to be received!")
    else:

        #chat_file = bot.get_file(update.message.document.file_id)
        chat_file = bot.get_file(item.file_id)

        # ================================================================
        # Send a file to BlueCLoud website
        # ================================================================

        url = 'http://riccardobruetesting.altervista.org/APIs/file/file_api.php'

        file_temp_pathname, headers = urllib.request.urlretrieve(chat_file["file_path"])
        file = open(file_temp_pathname, 'rb')
        files = {'file': (file_name, file)}

        values = {'userid': str(user_id), 'name': user_first_name}

        r = requests.post(url, files=files, data=values)

        print("__")
        print("File upload result: " + r.text)

        # ================================================================
        update.message.reply_text(r.text)


# ==============================================================================================
# ==============================================================================================

def openshiftStart():
    updater = Updater('521661539:AAHoy9AKdBccWEwsgNWKoZpAlJc33UuzROE')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.document, send_file))
    dispatcher.add_handler(MessageHandler(Filters.photo, send_file))
    dispatcher.add_handler(MessageHandler(Filters.audio, send_file))
    dispatcher.add_handler(MessageHandler(Filters.video, send_file))
    dispatcher.add_handler(MessageHandler(Filters.voice, send_file))

    updater.start_polling()
    updater.idle()


openshiftStart()
