import telebot
from extensions import APIException,CryptoConverter
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду в формате:\n'
            '<валюта> <валюта> <количество>\n'
            'Например: доллар евро 10\n'
            'Список валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты: доллар, евро, рубль'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text']) # Обработчик текстовых сообщений
def handle_text(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров')
        base, quote, amount = values
        amount = float(amount)
        total = CryptoConverter.get_price(base, quote, amount)
        text = f'{base} в {quote} - {total:.2f}'
        bot.send_message(message.chat.id,text)

    except APIException as e:
        bot.reply_to(message,f'Ошибка: {e}')
    except ValueError:
        bot.reply_to(message, 'Неправильный формат числа')
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка: {e}')

bot.polling(non_stop=True)