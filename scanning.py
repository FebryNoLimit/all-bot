import requests
import os
import datetime
import sys
import telebot

# Set expired date
expiration_date = datetime.datetime(2099, 2, 25)

# Check the current date
current_date = datetime.datetime.now()

# Compare the current date with the expiration date
if current_date > expiration_date:
    print("Script Expired. Hubungi FebryEnsz Untuk Mengupdate Script Di Github. Exit In 1 Second")
    sys.exit()

def dosl4():
  
def subdomainfin(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    response = requests.get(url)
    subdomains = response.text.strip().split("\n")
    return subdomains


def finder_v2(domain):
    subdomains = subdomainfin(domain)
    return subdomains


# Set up Telegram bot
bot_token = "6874070633:AAGPvbn0ECFMUJy6DwxF1movY2YODhsviTc"
bot = telebot.TeleBot(bot_token)

# Get allowed username from memory
allowed_username = "FebryPendosa123"

# Variable to track bot status
bot_active = True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Aku adalah bot Subdomain Finder Yang Dibuat Oleh @FebryPendosa123 . Jika Ingin Scan Maka Gunakan /scan <domain>")


@bot.message_handler(commands=['on'])
def turn_on(message):
    if message.from_user.username == allowed_username:
        global bot_active
        bot_active = True
        bot.reply_to(message, "Bot telah diaktifkan.")
    else:
        bot.reply_to(message, "Maaf, kamu tidak memiliki izin untuk mengaktifkan bot.")


@bot.message_handler(commands=['off'])
def turn_off(message):
    if message.from_user.username == allowed_username:
        global bot_active
        bot_active = False
        bot.reply_to(message, "Bot telah dinonaktifkan.")
    else:
        bot.reply_to(message, "Maaf, kamu tidak memiliki izin untuk menonaktifkan bot.")


@bot.message_handler(commands=['scan'])
def find_subdomains(message):
    if bot_active:
        domain = message.text.split()[1]
        subdomains = finder_v2(domain)
        if subdomains:
            result = "\n".join(subdomains)
            file_path = f"{domain}_subdomains.txt"
            with open(file_path, "w") as file:
                file.write(result)
            with open(file_path, "rb") as file:
                bot.send_document(message.chat.id, file)
            os.remove(file_path)
        else:
            bot.reply_to(message, "Tidak ditemukan subdomain untuk domain tersebut.")
    else:
        bot.reply_to(message, "Maaf, bot sedang dalam status nonaktif.")


# Start the bot
bot.polling()