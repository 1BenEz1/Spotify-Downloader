from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton
import logging

from trks import Tracks
from ytb import Ytb
import os , shutil
from con import Con


# Configuring logging to know what goes wrong and why
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)    

# configuring updater to connect to the bot
TOKEN = <TOKEN>
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher # easy access to the dispacher to add handlers

def help(update, context):
    re = "Usful Commands:\n"
    h_pl = "\n/start to change the playlist link\n"
    h_d = "\n/download to download the songs from the playlist\n" + "Notice: I'll only send you the newly added songs that I didn't send you already\n"
    h_ft = "\n/forgetTracks to delete the tracks record\n"
    h_fm = "\n/forgetMe to delete all your user record\n" + "Notice: I only save your telegram id, playlist link and what songs I already sent you\n"
    h_h = "\n/help to view all commands"
    reply = re + h_pl + h_d + h_ft + h_fm + h_h
    context.bot.send_message(chat_id=update.effective_chat.id, text = reply)

help_handler = CommandHandler('help',help)
dispatcher.add_handler(help_handler)


# Issueing the /start command
def start(update, context):
    user = update.message.from_user
    msg = "Hey " + f'{user.first_name}' +", send me the link to your playlist\nIf you don't know how look up how to share playlists"
    context.bot.send_message(chat_id=update.effective_chat.id, text = msg)

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)


# Configuring the user 
def updatePlayList(update, context):
    user_id = update.message.from_user.id
    playlist = update.message.text

    Con(user_id, playlist)

    update.message.reply_text('Great!')
    help(update, context)

updatePlayList_handler = MessageHandler(Filters.regex(r'^(https:\/\/open\.spotify\.com\/playlist.*)') , updatePlayList)
dispatcher.add_handler(updatePlayList_handler)


# download and send songs
def download(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text("I'm on it.. It might take a while")
    tracks = Tracks(user_id)
    songs = tracks.getTracks()
    yout = Ytb(songs)
    paths = yout.downloadSongs(user_id)
    for p in paths:
        context.bot.send_audio(chat_id = update.effective_chat.id, audio = open(p,'rb'))
        os.remove(p)

download_handler = CommandHandler('download', download)
dispatcher.add_handler(download_handler)


# delete all tracks records
def forgetTracks(update, context):
    user_id = update.message.from_user.id
    os.chdir(f'{user_id}') # enter dir
    os.remove('tracks.txt')
    os.chdir(os.pardir) # exit dir
    update.message.reply_text('Tracks record deleted')

forgetTracks_handler = CommandHandler('forgetTracks', forgetTracks)
dispatcher.add_handler(forgetTracks_handler)

# delete user record
def forgetMe(update, context):
    user_id = update.message.from_user.id
    dir_name = f"{user_id}"
    shutil.rmtree(dir_name)
    update.message.reply_text('User record deleted\nuse /start')

forgetMe_handler = CommandHandler('forgetMe', forgetMe)
dispatcher.add_handler(forgetMe_handler)

# Running the bot
updater.start_polling()

