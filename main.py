import telebot
import datetime
import os
import shutil

import json
from config import (
    PAYMENT_TOKEN, TELEGRAM_TOKEN,
    MODERATOR_ID, OWN_ID,
    )

from aiogram.types import ContentType

from pathlib import Path

from telebot.types import(
    Message,
    LabeledPrice,
    PreCheckoutQuery, 
    )

# Отправлять TXT файлы
# lkey2007 account


dp = telebot.TeleBot(TELEGRAM_TOKEN)
# bot = Bot(TELEGRAM_TOKEN, parse_mode='HTML')

# Цикл с отправкой всем пользователям
# Функция INFO, чтобы узнать текущую стоимость

class Message():
    def __init__(self, id):
        self.id = id
        self.images = list()
        self.subject = ''
        self.task = ''
        self.data = ''
        self.caption = ''

def check_block(id):
    try:
        path = Path(f"Data-Bases/Block-Users.json")

        # создать или оставить прежним
        path.touch(exist_ok=True)

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        status = True

    except json.decoder.JSONDecodeError:
        status = False
        print('File is empty')

    if status:

        if str(id) in data:
            return False

    return True


@dp.message_handler(commands=['start'])
def start_program(message):
    returning = check_block(message.chat.id)

    if returning:

        user_data = message.from_user
        dp.reply_to(message, f"Hi, {user_data.username} &#9996;\n&#127380; - {user_data.id} ", parse_mode="HTML")
        
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
                dp.send_message(message.chat.id, "&#128100; You are new user...", parse_mode="HTML")
                dp.send_message(message.chat.id, "To register, enter /lets_go &#128173;", parse_mode="HTML")

            else:
                dp.send_message(message.chat.id, "&#128159; You are old user!!!", parse_mode="HTML")
    
        else:
            dp.send_message(message.chat.id, "To register, enter /lets_go &#128173;", parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")

@dp.message_handler(commands=['lets_go'])
def register(message):
    returning = check_block(message.chat.id)

    if returning:
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
                dp.send_message(message.chat.id, "You have already been registered... &#128147;", parse_mode="HTML")
    
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
            dp.send_message(message.chat.id, f"You have been successully registered &#9786;\n&#129305; Current Week-Working is {datetime.datetime.today().strftime('%V-%B-%Y')}", parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")
    

@dp.message_handler(commands=['get_users_info'])
def send_unpaid(message):
    returning = check_block(message.chat.id)

    if returning:
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

        if status:
            for user in data:
                dp.send_message(message.chat.id, f"User - {data[user]['username']}\nFull Name - {data[user]['first_name']} {data[user]['last_name']}\nId - <code>{user}</code>\nStatus - {data[user]['status']}", parse_mode="HTML")

            dp.send_message(message.chat.id, "To block user enter /block and send his id...")

        else:
            dp.send_message(message.chat.id, "Empty")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")

@dp.message_handler(commands=['block'])
def get_block_user(message):
    returning = check_block(message.chat.id)

    if returning:
        if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:  
            dp.send_message(message.chat.id, "Send me id to block:")
    
            dp.register_next_step_handler(message, block_user)

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")


def block_user(message):
    returning = check_block(message.chat.id)

    if returning:
        try:
            path = Path(f"Data-Bases/{datetime.datetime.today().strftime('%V-%B-%Y')}.json")

            # создать или оставить прежним
            path.touch(exist_ok=True)

            with open(path, "r", encoding="utf-8") as file:
                data_users = json.load(file)

            status_global = True
        except json.decoder.JSONDecodeError:
            status_global = False
            print('File is empty')

        try:
            path = Path(f"Data-Bases/Block-Users.json")

            # создать или оставить прежним
            path.touch(exist_ok=True)

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            status = True

        except json.decoder.JSONDecodeError:
            status = False
            print('File is empty')

        if status_global:
            status_reg = True
            if status:
                
                if str(message.text) not in data and str(message.text) in data_users:
                    data[str(message.text)] = {}

                    data[str(message.text)]['first_name'] = data_users[str(message.text)]['first_name']
                    data[str(message.text)]['last_name'] = data_users[str(message.text)]['last_name']
                    data[str(message.text)]['username'] = data_users[str(message.text)]['username']

                else:
                    status_reg = False
                    dp.send_message(message.chat.id, "User alredy in blocked... &#128147;", parse_mode="HTML")
        
            else:
                data = {
                    str(message.text): {
                        "first_name": data_users[str(message.text)]['first_name'],
                        "last_name": data_users[str(message.text)]['last_name'],

                        "username": data_users[str(message.text)]['username'],
                    }
                }

            if status_reg:
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(data, file, sort_keys=True)
                
                dp.send_message(str(message.text), "You have been successfully blocked &#10060;", parse_mode="HTML")
                dp.send_message(message.chat.id, "User successully was blocked!")
                
        else:
            dp.send_message(message.chat.id, "System is empty")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")
 


@dp.message_handler(commands=['info'])
def information(message):
    returning = check_block(message.chat.id)

    if returning:

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

        if status:
            if str(user_data.id) not in data:
                dp.send_message(message.chat.id, "To learn more information enter /lets_go &#128173;", parse_mode="HTML")
            
            else:
                dp.send_message(message.chat.id, f"&#128187; Current Week-Working is {datetime.datetime.today().strftime('%V-%B-%Y')}...\nAnd You have registered on this week &#128583;", parse_mode="HTML")   
                current_price = int(600/len(data))
                if OWN_ID in data:
                    try:
                        current_price = int(600/(len(data)-1))
                    except:
                       current_price = int(600/len(data))

                dp.send_message(message.chat.id, f"&#127892; In this Week-Working have already registered <strong>{len(data)} people</strong>...\nSo, Current Price is <strong>{current_price}&#8381;</strong> for each person &#128176;", parse_mode="HTML")
                
                if not data[str(user_data.id)]['status']:
                    dp.send_message(message.chat.id, f"&#10060; You haven't paid this Week-Working...\n&#9999; Please indicate your nickname in the comments\nIf pay, click here: /pay &#128179;", parse_mode="HTML")

                else:
                    dp.send_message(message.chat.id, f"&#9989; You have successfully paid, thanks &#128537;", parse_mode="HTML")

        else:
            dp.send_message(message.chat.id, f"&#9989; No one has registered yet...\nTo registered enter /lets_go &#128173;", parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")

@dp.message_handler(content_types=ContentType.DOCUMENT)
def send_txt_file_id(message):
    
    if str(message.chat.id) != OWN_ID and str(message.chat.id) != MODERATOR_ID:
        status_send = False
        dp.send_message(message.chat.id, "I dont want send it :(", parse_mode="HTML")

    # dp.reply_to(message, "Message ID - "+str(dp.reply_to(message, "Message ID - "+str(message.chat.id))))
    
    try:
        if not os.path.exists("Downloads"): 
            os.makedirs("Downloads")

        path = Path(f"Downloads/{message.document.file_name}")

        # создать или оставить прежним
        path.touch(exist_ok=True)

        file_info = dp.get_file(message.document.file_id)
        downloaded_file = dp.download_file(file_info.file_path)

        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)

        dp.reply_to(message, "You can send another file\nOr send /run to proceed to adding information!")
    
    except Exception as _Ex:
        dp.send_message(message.chat.id, "Error has occurred :(\n"+str(_Ex), parse_mode="HTML")
    

    

@dp.message_handler(content_types=ContentType.PHOTO)
def send_photo_file_id(message: Message):
    # global message_by_1010205515
    returning = check_block(message.chat.id)

    if returning:


        dp.reply_to(message, "Message ID - "+str(message.chat.id))


        if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:
            try:
                # message_by_1010205515 = Message(str(message.chat.id))
                message_by_1010205515.images.append(str(message.photo[-1].file_id))
                # message_by_1010205515 = Message(message.photo[-1].file_id)

                message = dp.send_message(message.chat.id, "You can send photos\nOr send /go to proceed to adding information!")

                # dp.register_next_step_handler(message, process_subject_step)

                # dp.send_photo("1010205515", message.photo[-1].file_id)
            except Exception as _ex:
                dp.send_message(message.chat.id, 'An error has occurred\n'+str(_ex))

        else:

          dp.reply_to(message, f"Sorry :(\n I don't want to send it...")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")

    # создание экземпляра класса
@dp.message_handler(commands=['begin'])
def create_class(message):
    global message_by_1010205515

    returning = check_block(message.chat.id)

    if returning:


        dp.reply_to(message, "Message ID - "+str(message.chat.id))

        if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:

            message_by_1010205515 = Message(str(message.chat.id))
            # message_by_1010205515.images.append(str(message.photo[-1].file_id))
            # message_by_1010205515 = Message(message.photo[-1].file_id)

            message = dp.send_message(message.chat.id, "Please, send photos:\nClass was created!")

            # dp.send_photo("1010205515", message.photo[-1].file_id)

        else:

            dp.reply_to(message, f"Sorry :(\n I don't want to send it...")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")


# ввод информации
@dp.message_handler(commands=['go'])
def add_info(message):
    global message_by_1010205515

    if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:

        message = dp.send_message(message.chat.id, "Please, write subject: ")

        dp.register_next_step_handler(message, process_subject_step)

        # dp.send_photo("1010205515", message.photo[-1].file_id)

    else:

        dp.reply_to(message, f"Sorry :(\n I don't want to send it...")

@dp.message_handler(commands=['run'])
def add_info_file(message):
    global message_by_1010205515

    if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:

        message = dp.send_message(message.chat.id, "Please, write subject: ")

        message_by_1010205515 = Message(str(message.chat.id))

        dp.register_next_step_handler(message, process_subject_step_file)

    else:

        dp.reply_to(message, f"Sorry :(\n I don't want to send it...")


def process_subject_step(message):

    message_by_1010205515.subject = message.text

    message = dp.send_message(message.chat.id, "Please, write number or task: ")

    dp.register_next_step_handler(message, process_task_step)

def process_subject_step_file(message):

    message_by_1010205515.subject = message.text

    message = dp.send_message(message.chat.id, "Please, write number or task: ")

    dp.register_next_step_handler(message, process_task_step_file)

def process_task_step(message):

    message_by_1010205515.task = message.text

    message = dp.send_message(message.chat.id, "Please, Enter the date by which you want to complete the task ")

    dp.register_next_step_handler(message, process_date_step)

def process_task_step_file(message):

    message_by_1010205515.task = message.text

    message = dp.send_message(message.chat.id, "Please, Enter the date by which you want to complete the task ")

    dp.register_next_step_handler(message, process_date_step_file)

def process_date_step(message):
    
    message_by_1010205515.data = message.text

    message = dp.send_message(message.chat.id, "Please, write some description about it: ")

    dp.register_next_step_handler(message, process_caption_step)

def process_date_step_file(message):
    
    message_by_1010205515.data = message.text

    message = dp.send_message(message.chat.id, "Please, write some description about it: ")

    dp.register_next_step_handler(message, sending_files_with_caption)

def sending_files_with_caption(message):
    user_data = message.from_user
    message_by_1010205515.caption = message.text

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
    status_send = True

    if status and status_send:
        try:
            for user in data:
                returning = check_block(user)

                if returning and data[str(user)]['status']:
                # только те, у кого одобрена подписка
                    beauty_text = f"""
<b>ProGroup For</b> <i>{data[user]['username']}</i>&#127892;\n
<b>Subject:</b> {message_by_1010205515.subject}&#9999;
<b>Number or Task:</b> {message_by_1010205515.task}	&#128466;
<b>Date of completion:</b> {message_by_1010205515.data}&#128337;
<b>Additional Comment:</b> {message_by_1010205515.caption}&#128173;\n
&#8986;The work was done at: <u>{datetime.datetime.today().strftime('%A, %d %B %Y, %H:%M:%S')} (UTC+1)</u>
                """
                    # dp.send_document(str(user), document=message.document[-1].file_id, caption=beauty_text, parse_mode="HTML")

                    try:
                        # Отправляем кадый файл папки
                        for filename in os.listdir('./Downloads'):
                            print("FILE", filename)
                            with open(os.path.join('./Downloads', filename), 'rb') as file_send:
                                # update.message.reply_photo(file_send)
                                dp.send_document(str(user), document=file_send)

                        dp.send_message(str(user), beauty_text, parse_mode="HTML")

                        # Удаляем папку вместе со всеми ее файлами
                        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'./Downloads')
                        shutil.rmtree(path)
                            
                        dp.send_message(message.chat.id, f"The file was send { data[user]['username'] } &#128583;", parse_mode="HTML")

                    except Exception as _ex:
                        dp.send_message(message.chat.id, "&#9888; The process was fail\n"+str(_ex), parse_mode="HTML")

        except Exception as _ex:
            dp.send_message(message.chat.id, "Fail in send file\n"+str(_ex), parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, "No one has registered...)")


def process_caption_step(message):
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

    
    message_by_1010205515.caption = message.text
    if status:
        
        try:

            # Цикл отправки фото каждому пользователю
            for user in data:
                returning = check_block(user)

                if returning:
                # только те, у кого одобрена подписка
                
                    if data[str(user)]['status']:

                        beauty_text = f"""
<b>ProGroup For</b> <i>{data[user]['username']}</i>&#127892;\n
<b>Subject:</b> {message_by_1010205515.subject}&#9999;
<b>Number or Task:</b> {message_by_1010205515.task}	&#128466;
<b>Date of completion:</b> {message_by_1010205515.data}&#128337;
<b>Additional Comment:</b> {message_by_1010205515.caption}&#128173;\n
&#8986;The work was done at: <u>{datetime.datetime.today().strftime('%A, %d %B %Y, %H:%M:%S')} (UTC+1)</u>
                """
                        try:
                            for i in range(len(message_by_1010205515.images)):   
                                
                                if i == len(message_by_1010205515.images) - 1:
                                    dp.send_photo(str(user), photo=message_by_1010205515.images[i], caption=beauty_text, parse_mode='HTML')
                                
                                else:
                                    dp.send_photo(str(user), photo=message_by_1010205515.images[i])

                            dp.send_message(message.chat.id, f"The photo was send { data[user]['username'] } &#128583;", parse_mode="HTML")

                        except Exception as _ex:
                            dp.send_message(message.chat.id, "&#9888; The process was fail\n"+str(_ex), parse_mode="HTML")

            dp.send_message(message.chat.id, "The process was successful...)")
        
        except Exception as _ex:
            dp.send_message(message.chat.id, "The process was UNsuccessful...)\n"+str(_ex))

    else:
        dp.send_message(message.chat.id, "No one has registered...)")


@dp.message_handler(commands=['pay'])
def pay_process(message):
    returning = check_block(message.chat.id)

    if returning:
        user_data = message.from_user

        dp.send_message(message.chat.id, "&#128221; Your application is under consideration\nWhen the check is over, your status will change &#9989;", parse_mode="HTML")
    
        dp.send_message(OWN_ID, f'If "{user_data.username}" paid, send /add and this:')
        dp.send_message(MODERATOR_ID, f'If "{user_data.username}" paid, send /add and this:')
        
        id_text = f"<code>{user_data.id}</code>"

        dp.send_message(OWN_ID, id_text, parse_mode="HTML")
        dp.send_message(MODERATOR_ID, id_text, parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, "You Blocked &#10060;", parse_mode="HTML")


@dp.message_handler(commands=['add'])
def add_user(message):
    dp.send_message(message.chat.id,str( message.chat.id))

    if str(message.chat.id) == OWN_ID or str(message.chat.id) == MODERATOR_ID:  
        dp.send_message(message.chat.id, "Send me id:")
 
        dp.register_next_step_handler(message, get_id)

def get_id(message):

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

    if status:

        if str(message.text) in data:
            try:
                data[str(message.text)]['status'] = True
                
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(data, file, sort_keys=True)

                dp.send_message(str(message.text), "Your application has been approved &#9989;", parse_mode="HTML")
                
                dp.send_message(OWN_ID, f'Application of "{ data[str(message.text)] }" ({ str(message.text) }) was changed on {data[str(message.text)]["status"]} by "{ data[str(message.chat.id)]["username"] }" ({ str(message.chat.id) })')
                dp.send_message(MODERATOR_ID, f'Application of "{ data[str(message.text)] }" ({ str(message.text) }) was changed on {data[str(message.text)]["status"]} by "{ data[str(message.chat.id)]["username"] }" ({ str(message.chat.id) })')
            
 
            except Exception as _ex:
                dp.send_message(OWN_ID, "Fail\n"+str(_ex))
                dp.send_message(MODERATOR_ID, "Fail\n"+str(_ex))

        else:
            dp.send_message(OWN_ID, f"User is not exist\nWas get {message.text}")
            dp.send_message(MODERATOR_ID, f"User is not exist\nWas get {message.text}")


    else:
        dp.send_message(OWN_ID, "Empty")
        dp.send_message(MODERATOR_ID, "Empty")


# PAYMENT
PRICES = [
    LabeledPrice(label="Week-Working", amount=60000),
]


@dp.message_handler(commands=['buy'])
def buy_process(message):
    dp.send_message(message.chat.id, "Вы в разделе покупки", parse_mode="HTML")

    dp.send_invoice(

        message.chat.id,
        title="ProGroupShop",
        description="Week-Working",

        # токет сбера
        provider_token=PAYMENT_TOKEN,
        currency='rub',

        invoice_payload='some-invoice-payload-for-internal-use',

        need_email=False,
        need_phone_number=False,
        is_flexible=False,

        # все товары
        prices=PRICES,
        start_parameter='example',

        )

    # dp.send_invoice(
    #                  message.chat.id,  #chat_id
    #                  'Working Time Machine', #title
    #                  ' Want to visit your great-great-great-grandparents? Make a fortune at the races? Shake hands with Hammurabi and take a stroll in the Hanging Gardens? Order our Working Time Machine today!', #description
    #                  'HAPPY FRIDAYS COUPON', #invoice_payload
    #                  PAYMENT_TOKEN, #provider_token
    #                  'usd', #currency
    #                  PRICES, #prices
    #                  photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
    #                  photo_height=512,  # !=0/None or picture won't be shown
    #                  photo_width=512,
    #                  photo_size=512,
    #                  is_flexible=False,  # True If you need to set up Shipping Fee
    #                 )

# chat_id=chat_id, title="Flowers Delivery", description=description_of_package,
#                  invoice_payload='some-invoice-payload-for-internal-use',
#                  provider_token=keys.TEST_TRANZZO_PAYMENT, currency="UAH",
#                  prices=[{'label': 'flowers', 'amount': 1000}], start_parameter="test-start-parameter"
@dp.pre_checkout_query_handler(lambda q: True)
def checkout_process(pre_checkout_query: PreCheckoutQuery):
    dp.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
def successfully_payment(message: Message):
    dp.send_message(
        message.chat.id,
        f"All OKEY! {message.successful_payment.total_amount} {message.successful_payment.currency}"
    )


if __name__ == '__main__':
    print("MAIN")
    dp.polling(none_stop=True)