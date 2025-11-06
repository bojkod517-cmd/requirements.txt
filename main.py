from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 🔹 Токен бота (можно оставить прямо в коде)
TOKEN = "8445444619:AAFdR4jF1IQJzEFlL_DsJ-JTxT9nwkwwC58"
# 🔹 ID группы администраторов (замени на свою группу)
ADMIN_CHAT_ID = -1003120877184

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 🟢 Команда /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Рад тебя видеть! 💫\n"
        "Я — бот *Шепот сердец 💌*\n\n"
        "Можешь написать своё сообщение — администратор скоро тебе ответит.",
        parse_mode="Markdown"
    )

# 📨 Любое сообщение пользователя → в админ-группу
@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_to_admins(message: types.Message):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "без_юзернейма"
    text = f"📩 Сообщение от {username} (ID: {user_id}):\n\n{message.text or '[не текстовое сообщение]'}"
    await bot.send_message(ADMIN_CHAT_ID, text)

# 🔄 Если админ отвечает на сообщение → бот пересылает пользователю
@dp.message_handler(lambda msg: msg.chat.id == ADMIN_CHAT_ID and msg.reply_to_message)
async def reply_to_user(message: types.Message):
    try:
        original = message.reply_to_message.text
        user_id = int(original.split('ID:')[1].split(')')[0])
        await bot.send_message(user_id, message.text)
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")

if name == "main":
    executor.start_polling(dp, skip_updates=True)
