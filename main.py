from aiogram.types import ContentType, Message

import telebot

dp = telebot.TeleBot('5329546190:AAG_HZACSKKko30hk4hk9USu8tKrHQ6dGM4')

# @dp.message_handler(text='/album')
# async def send_album(message: Message):

#     album = MediaGroup()

#     album.attach_photo(photo=)

#     await message.answer_media_group(media=)



# @dp.message_handler(text='/photo')

# async def send_photo(message: Message):

#     chat_id = message.from_user.id

#     await dp.bot.send_photo(chat_id=chat_id, photo='')
 



@dp.message_handler(commands=['start'])
def start_program(message):
    user_data = message.from_user
    dp.reply_to(message, f"Hi, {user_data.username}\nYour id - {user_data.id}")


@dp.message_handler(content_types=ContentType.PHOTO)
def send_photo_file_id(message: Message):
 
    dp.send_photo('-1001731959960', message.photo[-1].file_id)


if __name__ == '__main__':
    dp.polling(none_stop=True)