from aiogram.types import ContentType, Message

import telebot
import datetime

dp = telebot.TeleBot('5329546190:AAG_HZACSKKko30hk4hk9USu8tKrHQ6dGM4')
group_id = '-1001731959960'

# @dp.message_handler(text='/album')
# async def send_album(message: Message):

#     album = MediaGroup()

#     album.attach_photo(photo=)

#     await message.answer_media_group(media=)



# @dp.message_handler(text='/photo')

# async def send_photo(message: Message):

#     chat_id = message.from_user.id

#     await dp.bot.send_photo(chat_id=chat_id, photo='')
 
class Message():
    def __init__(self, image):
        self.image = image
        self.subject = ''
        self.task = ''
        self.caption = ''


@dp.message_handler(commands=['start'])
def start_program(message):
    user_data = message.from_user
    dp.reply_to(message, f"Hi, {user_data.username}\nYour id - {user_data.id}")
    dp.send_message("1010205515", f"*ProGroup For* {user_data.username}\n*Subject:* {user_data.username}\n*Number or Task:* {user_data.username}\n*Additional Comment:* {user_data.username}", parse_mode='MarkdownV2'  )


@dp.message_handler(content_types=ContentType.PHOTO)
def send_photo_file_id(message: Message):
    global message_by_1010205515
    dp.reply_to(message, "Message ID - "+str(message.chat.id))


    if str(message.chat.id) == "1010205515":

        message_by_1010205515 = Message(message.photo[-1].file_id)

        message = dp.send_message(message.chat.id, "Please, write subject: ")

        dp.register_next_step_handler(message, process_subject_step)

        # dp.send_photo("1010205515", message.photo[-1].file_id)

    else:

        dp.reply_to(message, f"Sorry :(\n I don't want to send it...")

def process_subject_step(message):

    message_by_1010205515.subject = message.text

    message = dp.send_message(message.chat.id, "Please, write number or task: ")

    dp.register_next_step_handler(message, process_task_step)

def process_task_step(message):

    message_by_1010205515.task = message.text

    message = dp.send_message(message.chat.id, "Please, Enter the date by which you want to complete the task ")

    dp.register_next_step_handler(message, process_date_step)

def process_date_step(message):
    
    message_by_1010205515.caption = message.text

    message = dp.send_message(message.chat.id, "Please, write some description about it: ")

    dp.register_next_step_handler(message, process_caption_step)


def process_caption_step(message):
    user_data = message.from_user

    message_by_1010205515.caption = message.text


    beauty_text = f"""*ProGroup For* {user_data.username}\n
    *Subject:* {message_by_1010205515.subject}\n
    *Number or Task:* {message_by_1010205515.task}\n
    *Additional Comment:* {message_by_1010205515.caption}\n
    The work was done at: ***{datetime.datetime.today().strftime('%A, %d %B %Y, %H:%M:%S')}***"""

    dp.send_photo("1010205515", photo=message_by_1010205515.image, caption=beauty_text, parse_mode='MarkdownV2'  )

    dp.send_message(message.chat.id, "The process was successful...)")


if __name__ == '__main__':
    dp.polling(none_stop=True)