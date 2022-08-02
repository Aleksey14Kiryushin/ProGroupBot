from aiogram.types import ContentType, Message
from pathlib import Path

import telebot
import datetime
import json

dp = telebot.TeleBot('5329546190:AAG_HZACSKKko30hk4hk9USu8tKrHQ6dGM4')
group_id = '-1001731959960'

# Цикл с отправкой всем пользователям
# Функция INFO, чтобы узнать текущую стоимость

class Message():
    def __init__(self, image):
        self.image = image
        self.subject = ''
        self.task = ''
        self.data = ''
        self.caption = ''


@dp.message_handler(commands=['start'])
def start_program(message):
    user_data = message.from_user
    dp.reply_to(message, f"Hi, {user_data.username}\nYour id - {user_data.id}")
    
    try:
        path = Path(f"Data-Bases/{datetime.datetime.today().strftime('%V-%B-%Y')}.json")

        # создать или оставить прежним
        path.touch(exist_ok=True)

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        status = True
    except json.decoder.JSONDecodeError:
        status = False
        print('File is empty')
    
    # with open("Data-Bases/Data-Users.json", 'r') as j:
    #     data = json.loads(j.read())
    #     print("Data ",data)
    
    if status:
        # dp.send_message(message.chat.id, str(len(data)))

        if str(user_data.id) not in data:
            dp.send_message(message.chat.id, "You are new user...")
            dp.send_message(message.chat.id, "To register, enter /lets_go")

        else:
            dp.send_message(message.chat.id, "You are old user!!!")
 
    else:
        dp.send_message(message.chat.id, "To register, enter /lets_go")

@dp.message_handler(commands=['lets_go'])
def register(message):
    user_data = message.from_user

    try:
        path = Path(f"Data-Bases/{datetime.datetime.today().strftime('%V-%B-%Y')}.json")

        # создать или оставить прежним
        path.touch(exist_ok=True)

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        status = True
    except json.decoder.JSONDecodeError:
        status = False
        print('File is empty')
    
    status_reg = True

    if status:
        if str(user_data.id) not in data:
            data[str(user_data.id)] = {}

            data[str(user_data.id)]['status'] = False
            data[str(user_data.id)]['first_name'] = user_data.first_name
            data[str(user_data.id)]['last_name'] = user_data.last_name
            data[str(user_data.id)]['username'] = user_data.username

        else:
            status_reg = False
            dp.send_message(message.chat.id, "You have already been registered...")
 
    else:
        data = {
            str(user_data.id): {
                "status": False,

                "first_name": user_data.first_name,
                "last_name": user_data.last_name,

                "username": user_data.username,
            }
        }

    if status_reg:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, sort_keys=True)
        dp.send_message(message.chat.id, "You have been successully registered :)")



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
    
    message_by_1010205515.data = message.text

    message = dp.send_message(message.chat.id, "Please, write some description about it: ")

    dp.register_next_step_handler(message, process_caption_step)


def process_caption_step(message):
    user_data = message.from_user

    message_by_1010205515.caption = message.text

    try:

        beauty_text = f"""
        <b>ProGroup For</b> <i>{user_data.username}</i>\n
        <b>Subject:</b> {message_by_1010205515.subject}
        <b>Number or Task:</b> {message_by_1010205515.task}
        <b>Date of completion:</b> {message_by_1010205515.data}
        <b>Additional Comment:</b> {message_by_1010205515.caption}\n
The work was done at: <u>{datetime.datetime.today().strftime('%A, %d %B %Y, %H:%M:%S')} (UTC+1)</u>
        """

        dp.send_photo("1010205515", photo=message_by_1010205515.image, caption=beauty_text, parse_mode='HTML')

        dp.send_message(message.chat.id, "The process was successful...)")
    
    except Exception as _ex:
        dp.send_message(message.chat.id, "The process was UNsuccessful...)\n"+str(_ex))

if __name__ == '__main__':
    print("MAIN")
    dp.polling(none_stop=True)