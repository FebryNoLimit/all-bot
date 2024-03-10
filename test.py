import telebot
import os

bot = telebot.TeleBot("6874070633:AAGPvbn0ECFMUJy6DwxF1movY2YODhsviTc")

# Daftar pengguna premium
premium_users = ["FebryPendosa123"]

# Daftar admin
admin_users = ["FebryPendosa123"]

# Active Atau Off
bot_active = True

# Dictionary untuk melacak jumlah penggunaan perintah 'scan' oleh setiap pengguna
command_count = {}

# Finder
def subdomainfin(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    response = requests.get(url)
    subdomains = response.text.strip().split("\n")
    return subdomains


def finder_v2(domain):
    subdomains = subdomainfin(domain)
    return subdomains
    
# On
@bot.message_handler(commands=['on'])
def turn_on(message):
    if message.from_user.username == admin_users:
        global bot_active
        bot_active = True
        bot.reply_to(message, "Bot telah diaktifkan.")
    else:
        bot.reply_to(message, "Maaf, kamu tidak memiliki izin untuk mengaktifkan bot.")
@bot.message_handler(commands=['off'])
def turn_off(message):
    if message.from_user.username == admin_users:
        global bot_active
        bot_active = False
        bot.reply_to(message, "Bot telah dinonaktifkan.")
    else:
        bot.reply_to(message, "Maaf, kamu tidak memiliki izin untuk menonaktifkan bot.")


@bot.message_handler(commands=['reboot'])
def reboot(message):
    if message.from_user.username == admin_users:
        bot.reply_to(message, "Rebooting Bot ..")
        time.sleep(3)
        bot.reply_to(message, "Succes Reboot")
        sys.exit(1)
        os.system("python main.py")
# Handler untuk perintah /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if message.from_user.username in premium_users:
        bot.send_message(user_id, "Halo! Selamat datang di bot premium. Anda dapat menggunakan perintah 'scan' tanpa batasan.")
        command_count[user_id] = 0
    else:
        bot.send_message(user_id, "Halo! Selamat datang di bot. Anda hanya dapat menggunakan perintah 'scan' hingga 10 kali.")
        command_count[user_id] = 0

# Handler untuk perintah /scan
@bot.message_handler(commands=['scan'])
def find_subdomains(message):
    user_id = message.from_user.id
    if message.from_user.username in premium_users or command_count[user_id] < 10:
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
                command_count[user_id] += 1
            else:
                bot.reply_to(message, "Tidak ditemukan subdomain untuk domain tersebut.")
        else:
            bot.reply_to(message, "Maaf, bot sedang dalam status nonaktif.")
    else:
        bot.reply_to(message, "Anda telah mencapai batas penggunaan perintah 'scan'.")

# Handler untuk perintah /add
@bot.message_handler(commands=['add'])
def add_premium(message):
    user_id = message.from_user.id
    if message.from_user.username in admin_users:
        if message.reply_to_message is not None:
            added_user_id = message.reply_to_message.from_user.id
            if added_user_id not in premium_users:
                premium_users.append(added_user_id)
                bot.send_message(user_id, "Pengguna telah ditambahkan ke daftar pengguna premium.")
            else:
                bot.send_message(user_id, "Pengguna sudah ada dalam daftar pengguna premium.")
        else:
            bot.send_message(user_id, "Mohon reply ke pesan pengguna yang ingin ditambahkan ke daftar premium.")
    else:
        bot.send_message(user_id, "Anda tidak memiliki izin untuk menggunakan perintah '/add'.")

bot.polling()