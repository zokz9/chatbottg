from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
import telebot

# Токен вашего бота (полученный от BotFather)
TOKEN = 'Токен botfather'
bot = telebot.TeleBot(TOKEN)

# Авторизация в GigaChat
llm = GigaChat(
    credentials="Ключ GigaChatAPI",
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
)

messages = [
    SystemMessage(
        content="Ты — полезный помощник. Отвечай на вопросы пользователя."
    )
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот. Как я могу помочь?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global messages
    user_input = message.text
    messages.append(HumanMessage(content=user_input))
    res = llm.invoke(messages)
    messages.append(res)
    bot.reply_to(message, res.content)

# Запуск бота
bot.infinity_polling()
