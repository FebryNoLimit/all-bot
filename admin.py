import telebot
import time
import requests
import socket
import threading
import subprocess

# Token bot Anda
TOKEN = '6993044367:AAGDk7mvPdj9OP8dVqp3v5yzlsa5sZirpPA'

# Daftar admin yang dapat mengontrol bot
admin_list = ['FebryPendosa123']

# Inisialisasi bot
bot = telebot.TeleBot(TOKEN)

# Fungsi untuk memeriksa apakah pengguna adalah admin
def is_admin(user):
    return user.username in admin_list

@bot.message_handler(commands=['start'])
def utama(message):
    bot.reply_to(message, '''
Hallo Saya Admin Bot Yang Dibuat Oleh @FebryPendosa123 Dan Berfungsi Untuk Grup Kalian''')
# Perintah untuk mengaktifkan bot
@bot.message_handler(commands=['on'])
def turn_on(message):
    if is_admin(message.from_user):
        # Mengaktifkan bot
        bot_enabled = True
        bot.reply_to(message, 'Bot telah diaktifkan')
    else:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk mengaktifkan bot')

# Perintah untuk mematikan bot
@bot.message_handler(commands=['off'])
def turn_off(message):
    if is_admin(message.from_user):
        # Mematikan bot
        bot_enabled = False
        bot.reply_to(message, 'Bot telah dimatikan')
    else:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk mematikan bot')

# Perintah untuk memuat ulang bot
@bot.message_handler(commands=['reboot'])
def reboot(message):
    if is_admin(message.from_user):
        # Memuat ulang bot
        bot.reply_to(message, 'Bot sedang dimuat ulang')
        # Tambahkan logika pembaruan atau pemulihan bot di sini
    else:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk memuat ulang bot')

# Perintah untuk melakukan pin pesan
@bot.message_handler(commands=['pin'])
def pin_message(message):
    if message.reply_to_message:
        if is_admin(message.from_user):
            # Melakukan pin pesan
            bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        else:
            bot.reply_to(message, 'Anda tidak memiliki izin untuk melakukan pin pesan')
    else:
        bot.reply_to(message, 'Anda harus membalas pesan untuk melakukan pin')

# Perintah untuk menambahkan admin
@bot.message_handler(commands=['add'])
def add_admin(message):
    if is_admin(message.from_user):
        if message.reply_to_message:
            new_admin = message.reply_to_message.from_user.username
            if new_admin not in admin_list:
                admin_list.append(new_admin)
                bot.reply_to(message, f'{new_admin} telah ditambahkan ke daftar admin')
            else:
                bot.reply_to(message, f'{new_admin} sudah ada dalam daftar admin')
        else:
            bot.reply_to(message, 'Anda harus membalas pesan pengguna untuk menambahkan admin')
    else:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk menambahkan admin')

@bot.message_handler(commands=['listadmin'])
def list_admin(message):
    admin_names = [admin for admin in admin_list]
    admin_names_str = '\n'.join(admin_names)
    bot.reply_to(message, f"Daftar admin:\n{admin_names_str}")

# Menjalankan bot
bot_enabled = False
bot.polling()