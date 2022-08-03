import telebot
import datetime
import json
from config import PAYMENT_TOKEN, TELEGRAM_TOKEN, ITEM_URL, OWN_ID

from aiogram.types import ContentType

from pathlib import Path

from telebot.types import(
    Message,
    LabeledPrice,
    PreCheckoutQuery, 
    )


dp = telebot.TeleBot(TELEGRAM_TOKEN)
# bot = Bot(TELEGRAM_TOKEN, parse_mode='HTML')

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

@dp.message_handler(commands=['info'])
def information(message):
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
            dp.send_message(message.chat.id, "To learn more information enter /lets_go &#128173;")
        
        else:
            dp.send_message(message.chat.id, f"&#128187; Current Week-Working is {datetime.datetime.today().strftime('%V-%B-%Y')}...\nAnd You have registered on this week &#128583;", parse_mode="HTML")
            dp.send_message(message.chat.id, f"&#127892; In this Week-Working have already registered {len(data)} people...\nSo, Current Price is {int(600/len(data))}&#8381; for each person &#128176;", parse_mode="HTML")
            
            if not data[str(user_data.id)]['status']:
                dp.send_message(message.chat.id, f"&#10060; You haven't paid this Week-Working...\n&#9999; Please indicate your nickname in the comments\nIf pay, click here: /pay &#128179;", parse_mode="HTML")

            else:
                dp.send_message(message.chat.id, f"&#9989; You have successfully paid, thanks &#128537;", parse_mode="HTML")

    else:
        dp.send_message(message.chat.id, f"&#9989; No one has registered yet...\nTo registered enter /lets_go &#128173;", parse_mode="HTML")


@dp.message_handler(content_types=ContentType.PHOTO)
def send_photo_file_id(message: Message):
    global message_by_1010205515
    dp.reply_to(message, "Message ID - "+str(message.chat.id))


    if str(message.chat.id) == OWN_ID:

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

                        dp.send_photo(str(user), photo=message_by_1010205515.image, caption=beauty_text, parse_mode='HTML')
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
    user_data = message.from_user

    dp.send_message(message.chat.id, "&#128221; Your application is under consideration\nWhen the check is over, your status will change &#9989;", parse_mode="HTML")
   
    dp.send_message(OWN_ID, f'If "{user_data.username}" paid, send /add and this:')
    
    dp.send_message(OWN_ID, str(user_data.id))

@dp.message_handler(commands=['add'])
def add_user(message):
    
    if str(message.chat.id) == OWN_ID:  
        dp.send_message(OWN_ID, "Send me id:")
 
        dp.register_next_step_handler(message, get_id)

def get_id(message):
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

        if str(message.text) in data:
            try:
                data[str(message.text)]['status'] = True
                
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(data, file, sort_keys=True)

                dp.send_message(str(message.text), "Your application has been approved &#9989;", parse_mode="HTML")
                
                dp.send_message(OWN_ID, "All Okey!!!")
 
            except Exception as _ex:
                dp.send_message(OWN_ID, "Fail\n"+str(_ex))

        else:
            dp.send_message(OWN_ID, f"User is not exist\nWas get {message.text}")


    else:
        dp.send_message(OWN_ID, "Empty")


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

    dp.send_invoice(
                     message.chat.id,  #chat_id
                     'Working Time Machine', #title
                     ' Want to visit your great-great-great-grandparents? Make a fortune at the races? Shake hands with Hammurabi and take a stroll in the Hanging Gardens? Order our Working Time Machine today!', #description
                     'HAPPY FRIDAYS COUPON', #invoice_payload
                     PAYMENT_TOKEN, #provider_token
                     'usd', #currency
                     PRICES, #prices
                     photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
                     photo_height=512,  # !=0/None or picture won't be shown
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                    )

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