import telebot
from flask import Flask, request

TOKEN = "7974881474:AAHOzEfo2pOxDdznJK-ED9tGikw6Yl7jZDY"
OWNER_ID = 14703890051

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Привіт! Надішли мені свій відгук, і я передам його адміну 😉")

@bot.message_handler(func=lambda m: True)
def feedback(msg):
    bot.send_message(OWNER_ID, f"Новий відгук від @{msg.from_user.username or msg.from_user.first_name}:\n\n{msg.text}")
    bot.reply_to(msg, "✅ Дякую! Відгук передано адміну.")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://review-bot-i3kh.onrender.com/' + TOKEN)
    return "Бот запущений!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
