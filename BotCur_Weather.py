import telebot
from config import TOKEN, keys
from extensions import BotException, BotLogic

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Чтобы начать работу, введите через пробел команду, следующего формата:\n' \
'<исходная валюта>\n<валюта перевода>\n<количество>\nРегистр значения не имеет\nЧтобы увидеть список доступных валют, введите:\n/currencies\n' \
           'Также можете узнать погоду в интересующем вас городе, просто вписав его название одним словом.\n' \
           'Если название города состоит из 2 и более слов - просто соедините их дефисом :)'
    bot.reply_to(message, f"Hello {message.chat.username}\n {text}")

@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text,i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    param = message.text.split(' ')
    if len(param) == 1:
        try:
            text = BotLogic.weather(param)
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n {e}\n или не верно введено название Города\n попробуйте еще раз или введите:\n/help')
        else:
            bot.send_message(message.chat.id, text)
    else:
        try:
            if len(param) != 3:
                raise BotException('Введите 3 обязательных параметра запроса')
            base_cur, p_cur, value = message.text.title().split(' ')
            total = BotLogic.convert(base_cur, p_cur, value)
        except BotException as e:
            bot.reply_to(message, f'Ошибка пользователя\n {e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n {e}')
        else:
            text = f'Цена {value} {keys[base_cur]} составляет --> {total} {keys[p_cur]} '
            bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
