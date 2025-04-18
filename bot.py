import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_news, approve_news, reject_news, init_db

init_db()

SITE_URL = "http://127.0.0.1:5000/"
BOT_TOKEN = '7933023765:AAHOHT0AuKPkVDzagc1ZLJLmw196TBJPHXE'
MODERATOR_ID = 1874487891
MODERATOR_ID1 = 1775908002

bot = telebot.TeleBot(BOT_TOKEN)
pending_news = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши новость, и мы отправим её на модерацию.")

@bot.message_handler(func=lambda m: True)
def receive_news(message):
    news_id = add_news(message.from_user.username, message.text)
    pending_news[news_id] = message.from_user.id

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Принять", callback_data=f"accept_{news_id}"),
        InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{news_id}")
    )

    bot.send_message(MODERATOR_ID,
                     f"Новая новость от @{message.from_user.username}:\n\n{message.text}",
                     reply_markup=markup)

    bot.send_message(MODERATOR_ID1,
                     f"Новая новость от @{message.from_user.username}:\n\n{message.text}",
                     reply_markup=markup)

    global text, au
    au = f"{message.from_user.username}"
    text = f"{message.text}"

@bot.callback_query_handler(func=lambda call: call.data.startswith(('accept_', 'reject_')))
def handle_moderation(call):
    action, news_id = call.data.split("_")
    news_id = int(news_id)
    user_id = pending_news.get(news_id)

    if action == "accept":
        approve_news(news_id)

        t = {'title':text, 'content': au}
        with open("news.json", "rt", encoding="utf8") as f:
            news_list = json.loads(f.read())
        news_list['news'].append(t)

        with open('news.json', 'w') as news_file:
            json.dump(news_list, news_file)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📎 Перейти к новости", url=SITE_URL))

        bot.send_message(user_id, "🎉 Ваша новость одобрена и опубликована!", reply_markup=markup)
    else:
        reject_news(news_id)
        bot.send_message(user_id, "❌ Ваша новость отклонена модератором.")


    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)


bot.polling()
