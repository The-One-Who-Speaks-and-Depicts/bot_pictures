from model import StyleTransferModel
from telegram_token import token
from config import start_message, text_response_message
import numpy as np
from PIL import Image
from io import BytesIO

# В бейзлайне пример того, как мы можем обрабатывать две картинки, пришедшие от пользователя.
# При реалиазации первого алгоритма это Вам не понадобится, так что можете убрать загрузку второй картинки.
# Если решите делать модель, переносящую любой стиль, то просто вернете код)

model = StyleTransferModel()
content_image_file = {}


def send_prediction_on_photo(bot, update):
    # Нам нужно получить две картинки, чтобы произвести перенос стиля, но каждая картинка приходит в
    # отдельном апдейте, поэтому в простейшем случае мы будем сохранять id первой картинки в память,
    # чтобы, когда уже придет вторая, мы могли загрузить в память уже сами картинки и обработать их.
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
	content_image_file[chat_id] = image_file
	content_image_stream = BytesIO()
	content_image_file[chat_id].download(out=content_image_stream)
	del content_image_file[chat_id]

	output = model.transfer_style(content_image_stream)

        # теперь отправим назад фото
	output_stream = BytesIO()
	output.save(output_stream, format='PNG')
	output_stream.seek(0)
	bot.send_photo(chat_id, photo=output_stream)
    
    


if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters
    import logging
	
    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало.
    # если есть проблемы с подключением, то попробуйте убрать прокси или сменить на другой
    # проекси ищется в гугле как "socks4 proxy"
    updater = Updater(token=token,  request_kwargs={'proxy_url': 'socks4://95.110.227.5:64409'})

    # В реализации большого бота скорее всего будет удобнее использовать Conversation Handler
    # вместо назначения handler'ов таким способом
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
	updater.dispatcher.add_handler(MessageHandler(Filters.command("Start"), send_message(message.chat.id, start_message))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, send_message(message.chat.id, text_response_message))
	updater.start_polling()
	
  
