import telebot
import re

bot = telebot.TeleBot('...')
value = ''
prev_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('CE', callback_data='CE'),
             telebot.types.InlineKeyboardButton('C', callback_data='C'),
             telebot.types.InlineKeyboardButton('<=', callback_data='<='),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton('+-', callback_data='+-'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton('.', callback_data='.'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=["start"])
def start(message):
    global value
    if value == '':
        bot.send_message(message.chat.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, value, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global value, prev_value
    if call.data == 'CE':
        value = ''.join(re.split(r'[\*\/\+\-]', value)[:-1])
    elif call.data == 'C':
        value = ''
    elif call.data == '<=':
        if value != '':
            value = value[:-1]
    elif call.data == '+-':
        if value[0] == '-':
            value = value[1:]
        else:
            value = '-' + value
    elif call.data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'Ошибка!'
    else:
        value += call.data

    if value != prev_value:
        if value == '':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='0',
                                  reply_markup=keyboard)
            prev_value = '0'
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=value,
                                  reply_markup=keyboard)
            prev_value = value

    if value == 'Ошибка!':
        value = ''


bot.polling(none_stop=True, interval=0)
