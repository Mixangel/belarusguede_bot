import telebot
from telebot import types
import sqlite3
import os

# Токен вашего бота (или берется из системных переменных хостинга)
TOKEN = os.getenv("TOKEN", "8869832666: AAGEOc6gqFIOPjyJ_Not0kdR9nxSCX7If6k")
bot = telebot.TeleBot(TOKEN)


# Функция для получения фактов из БД
def get_db_info():
    conn = sqlite3.connect('belarus_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, description FROM references_info")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📖 Справочник по РБ")
    btn2 = types.KeyboardButton("🧠 Викторина")
    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}! 🇧🇾\n"
        "Этот бот создан для изучения историко-культурного наследия и проверки знаний о Республике Беларусь.",
        reply_markup=markup
    )


# Обработка текстовых кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📖 Справочник по РБ":
        infos = get_db_info()
        response = "<b>Информационный справочник:</b>\n\n"
        for title, desc in infos:
            response += f"🔹 <b>{title}</b>\n{desc}\n\n"
        bot.send_message(message.chat.id, response, parse_mode="HTML")

    elif message.text == "🧠 Викторина":
        # Простой пример вопроса викторины из БД
        conn = sqlite3.connect('belarus_project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT question, option1, option2, option3, correct_option FROM quiz LIMIT 1")
        q = cursor.fetchone()
        conn.close()

        if q:
            question_text, opt1, opt2, opt3, correct = q
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(opt1, callback_data="opt_1"))
            markup.add(types.InlineKeyboardButton(opt2, callback_data="opt_2"))
            markup.add(types.InlineKeyboardButton(opt3, callback_data="opt_3"))

            bot.send_message(message.chat.id, f"<b>Вопрос викторины:</b>\n{question_text}", reply_markup=markup,
                             parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "Вопросы пока не добавлены в базу данных.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню.")


if __name__ == '__main__':
    print("Бот запущен на сервере...")
    bot.infinity_polling()