import random
import array
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main.settings.settings import *
# from twilio.rest import Client
import logging

logger = logging.getLogger(__file__)


class BaseStatusClass:
    @classmethod
    def vars_to_dict(cls) -> dict:
        valid_vars = {
            var: value
            for var, value in cls.__dict__.items()
            if not callable(getattr(cls, var)) and not var.startswith("__")
        }
        return valid_vars

    @classmethod
    def get_tuples_for_choices(cls) -> list:
        return [
            (value, value)
            for var, value in cls.__dict__.items()
            if not callable(getattr(cls, var)) and not var.startswith("__")
        ]

    @classmethod
    def get_list_for_choices(cls) -> list:
        return [
            value
            for var, value in cls.__dict__.items()
            if not callable(getattr(cls, var)) and not var.startswith("__")
        ]


def auto_generate_password():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
               '*', '(', ')', '<']

    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
        password = password + x

    # print out password
    return password


def str2bool(v):
    if type(v) == bool:
        return v
    return v.lower() in ("yes", "true", "t", "1")


def send_mail(to_email, subject=None, text_message=None, html_message=None):
    # me == my email address
    # you == recipient's email address
    from_email = EMAIL_CONFIG["sender_email"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Create the body of the message (a plain-text and an HTML version).
    text = text_message
    html = html_message

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL(host=EMAIL_CONFIG["host"], port=EMAIL_CONFIG["port"])
    s.login(from_email, EMAIL_CONFIG["sender_password"])
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()


def validate_and_format_phone_number(phone_number):
    """
        phone_number: phone number in the string format to clean and validate
    """
    if not phone_number:
        return None

    cleaned_phone_number = re.sub('[^0-9\+]', '', phone_number)
    if len(cleaned_phone_number) < 10:
        return None

    elif len(cleaned_phone_number) == 10:
        if not cleaned_phone_number.startswith('+1'):
            return '+1' + cleaned_phone_number

        return None

    elif len(cleaned_phone_number) == 12:
        if cleaned_phone_number.startswith('+1'):
            return cleaned_phone_number

        return None

    return None


def send_sms(to_phone_number, message):
    valid_to_phone_number = validate_and_format_phone_number(to_phone_number)
    if not valid_to_phone_number:
        logger.error('Invalid phone number to send message:: ' + str(to_phone_number))
        return

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_KEY
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=message,
                                     from_=TWILIO_FROM_PHONE_NUMBER,
                                     to=valid_to_phone_number)

    if message and message.sid:
        logger.info('Sent sms to: ' + str(valid_to_phone_number))
        return

    logger.error('Could not send sms to: ' + str(valid_to_phone_number))
    logger.error('Message:: ' + str(message.sid))


def generate_nlg(response_string, dictionary):
    text_response = response_string
    for item in dictionary.keys():
        # sub item for item's paired value in string
        text_response = re.sub('{' + item + '}', str(dictionary[item]), text_response)
    return text_response


if __name__ == '__main__':
    # password = auto_generate_password()
    # print(password)
    send_sms(to_phone_number='+919916778133', message='Hello, this is test sms')
