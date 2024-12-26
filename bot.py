import os
import telebot
import configparser
import pandas as pd

# Вставьте ваш токен Telegram-бота
TOKEN = "7654163179:AAHFxQUX9NL4wBjuGKQ5BvknHZXGqznsA6c"  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

# Пути к файлам конфигурации
CONFIG_FILE = "config.data"

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я ваш помощник.\n\nДоступные команды:\n"
                          "/setup - Настроить конфигурацию API\n"
                          "/merge - Объединить два CSV файла\n"
                          "/update - Обновить инструмент\n"
                          "/install - Установить зависимости\n"
                          "/help - Помощь")

# Команда /setup
@bot.message_handler(commands=["setup"])
def setup(message):
    try:
        msg = bot.reply_to(message, "Введите API ID:")
        bot.register_next_step_handler(msg, process_api_id)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

def process_api_id(message):
    api_id = message.text
    bot.reply_to(message, "Введите Hash ID:")
    bot.register_next_step_handler(message, process_hash_id, api_id)

def process_hash_id(message, api_id):
    hash_id = message.text
    bot.reply_to(message, "Введите номер телефона:")
    bot.register_next_step_handler(message, save_config, api_id, hash_id)

def save_config(message, api_id, hash_id):
    phone = message.text
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    cpass.set('cred', 'id', api_id)
    cpass.set('cred', 'hash', hash_id)
    cpass.set('cred', 'phone', phone)
    with open(CONFIG_FILE, 'w') as setup:
        cpass.write(setup)
    bot.reply_to(message, "Конфигурация сохранена!")

# Команда /merge
@bot.message_handler(commands=["merge"])
def merge(message):
    bot.reply_to(message, "Отправьте первый CSV файл:")
    bot.register_next_step_handler(message, get_first_csv)

def get_first_csv(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("file1.csv", "wb") as f:
            f.write(downloaded_file)
        bot.reply_to(message, "Отправьте второй CSV файл:")
        bot.register_next_step_handler(message, get_second_csv)
    except Exception as e:
        bot.reply_to(message, f"Ошибка загрузки файла: {e}")

def get_second_csv(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("file2.csv", "wb") as f:
            f.write(downloaded_file)

        bot.reply_to(message, "Начинаю объединение файлов...")
        file1 = pd.read_csv("file1.csv")
        file2 = pd.read_csv("file2.csv")
        merged = file1.merge(file2, on="username")
        merged.to_csv("output.csv", index=False)

        with open("output.csv", "rb") as f:
            bot.send_document(message.chat.id, f)

        bot.reply_to(message, "Объединение завершено! Отправил результат.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при объединении файлов: {e}")

# Команда /update
@bot.message_handler(commands=["update"])
def update(message):
    try:
        bot.reply_to(message, "Обновляю инструмент...")
        os.system("""
            curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/add2group.py
            curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/scraper.py
            curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/setup.py
            curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/smsbot.py
            chmod 777 *.py
        """)
        bot.reply_to(message, "Инструмент обновлён!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка обновления: {e}")

# Команда /install
@bot.message_handler(commands=["install"])
def install(message):
    try:
        bot.reply_to(message, "Устанавливаю зависимости...")
        os.system("""
            pip3 install telethon requests configparser pandas numpy cython
        """)
        bot.reply_to(message, "Зависимости установлены!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка установки зависимостей: {e}")

# Команда /help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.reply_to(message, "Доступные команды:\n"
                          "/setup - Настроить конфигурацию API\n"
                          "/merge - Объединить два CSV файла\n"
                          "/update - Обновить инструмент\n"
                          "/install - Установить зависимости\n"
                          "/help - Помощь")

# Запуск бота
bot.polling()
