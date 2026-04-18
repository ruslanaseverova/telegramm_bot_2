import telebot
from config import TOKEN
import os
from classification import detect 

# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot(TOKEN)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


@bot.message_handler(commands=['start', "play"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(content_types=["photo"])
def send_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, "Изображение не получено")
    info = bot.get_file(message.photo[-1].file_id)
    name = info.file_path.split("/")[-1]
    save_file = bot.download_file(info.file_path)
    with open(name, "wb") as f:
        f.write(save_file)
    # Классификация
    class_name, proc = detect(f"./{name}", "./models/keras_model.h5", "./models/labels.txt")
    if  proc >= 50:
        bot.send_message(message.chat.id, f"На изображении найден {class_name} с вероятностью {proc}%")
    else:
        bot.send_message(message.chat.id, f"Изображение не распознано")
    os.remove(f"./{name}")

bot.polling()