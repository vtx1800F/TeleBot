import telebot
from config import keys, token
from extensions import ConvertionException, CryptoConverter

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])
def help (message: telebot.types.Message):
    text= 'Что бы начать работу, введите команду в следующем формате:\n <Имя валюты> \ ' \
'<В какую валюту перевести>\
<Колличество переводимой валюты>\n Увидеть список всех доступных валют : /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values= message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

            quote, base, amount = values
            total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. ')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. ')
    else:
        text=f'Цена {amount} {quote} в {base}-{total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()