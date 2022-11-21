import telebot
import requests

url = ''
bot = telebot.TeleBot('...')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, '\U0001F44B Привет! Отправьте мне ссылку на сайт и я проверю его доступность.')


@bot.message_handler(content_types=["text"])
def check_url(message):
    response = None
    global url
    if message.text.find('http') == -1:
        url = 'https://' + message.text
    else:
        url = message.text
    try:
        response = requests.get(url)
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='\U0001F44C Да!', callback_data='yes');
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='\U000026D4 Как-нибудь потом.', callback_data='no');
        keyboard.add(key_no)
        bot.send_message(message.chat.id, '\U00002705 Сайт доступен, хотите перейти на него?', reply_markup=keyboard)
    except:
        if response is not None:
            bot.send_message(message.chat.id, '\U0000274C Сайт в настоящее время недоступен и вернул HTTP ответ:',
                             response.status_code)
        else:
            bot.send_message(message.chat.id, '\U00002757 Проверьте введенные Вами данные!')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        keyboard = types.InlineKeyboardMarkup()
        button_url = types.InlineKeyboardButton(text=f'{url}', url=f'{url}')
        keyboard.add(button_url)
        bot.send_message(call.message.chat.id, '\U0000270B Досвидания!', reply_markup=keyboard)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, '\U0001F914 Как хотите.')


bot.polling(none_stop=True, interval=0)
