import telebot
import re
from collections import Counter

preposition = '''что, будто, если, когда, словно, чтобы, как, ибо, пока, и, тоже, также, ни, а, но, однако,
зато, же, только, или, либо, то, когда, пока, едва, лишь, вследствие, как, точно, будто, 
чтобы, дабы, если, когда, коли, ежели, раз, хотя, поэтому, потому'''
current_page = 1
pages = 1
words = []

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('<', callback_data='<'),
             telebot.types.InlineKeyboardButton('' + str(current_page), callback_data=' '),
             telebot.types.InlineKeyboardButton('>', callback_data='>'))

bot = telebot.TeleBot('...')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'U0001F44B Привет! Пришлите мне текст и я составлю по нему статистику.')


@bot.message_handler(content_types=["text"])
def analyzer(message):
    global words
    text = message.text
    words = list(filter(None, re.split(r'[\s!\,\.:\—\?\-\;\(\)]+', text)))
    current_page = 1
    pages = 1

    update_stat(message, False)

    clean_words = filter(lambda w: w not in preposition, words)
    bot.send_message(message.chat.id, 'Самое популярные слова:\n' + '\n'.join(
        (c[0] + ' - ' + str(c[1]) + ' раз(а)') for c in Counter(clean_words).most_common(5)))
    bot.send_message(message.chat.id, 'Самое длинное:\n' + max(words, key=len))

    if text.strip()[-1] == '.':
        bot.send_message(message.chat.id, 'Количество предложений: ' + str(message.text.count('.')))
    else:
        bot.send_message(message.chat.id, 'Количество предложений: ' + str(message.text.count('.') + 1))


@bot.callback_query_handler(func=lambda call: True)
def turn_page(call):
    global current_page
    if call.data == '>' and current_page != pages:
        current_page += 1
        update_stat(call, True)
    elif call.data == '<' and current_page != 1:
        current_page -= 1
        update_stat(call, True)


def update_stat(message, isUpdate):
    global current_page
    global pages
    global words

    pages = len(words) // 20 + 1
    l = len(''.join(words))
    result = []

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('<', callback_data='<'),
                 telebot.types.InlineKeyboardButton('' + str(current_page), callback_data=' '),
                 telebot.types.InlineKeyboardButton('>', callback_data='>'))

    for w in words[(current_page - 1) * 20:current_page * 20]:
        result.append(w + ' - {0:.2f}%\n'.format(len(w) / l * 100))

    if isUpdate == False:
        bot.send_message(message.chat.id, ''.join(result), reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                              text=''.join(result), reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
