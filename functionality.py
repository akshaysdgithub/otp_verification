import re
import time
import email
import random
import imaplib
import smtplib
import streamlit as st
from logger import logging
from config import settings
from email.message import EmailMessage
# from encodings.utf_8 import decode


## Generate Random 6-Digit Number
def generate_otp():
    otp=random.randint(100000,999999)
    return otp


## Time counting func in seconds
def streamlit_count_down(ts):
    with st.empty():
        ts += 1
        while ts>0:
            ts -= 1
            mins, secs=divmod(ts,60)
            time_now=f"{mins:02d}:{secs:02d}"
            st.header(f"{time_now}")
            time.sleep(1)


## Validate Email Syntax
def validate_email(email_str:str, otp_msg_placeholder):
    logging.info("Email Validation Started.")
    d=email_str.split()
    if len(d)==0:
        logging.info("No Email String Detected.")
        otp_msg_placeholder.info("Invalid Email")
        return False, None
    elif len(d)!=1:
        logging.info("Multiple Email String Detected.")
        otp_msg_placeholder.info("Invalid Email")
        return False, None
    else:
        email_str=d[0].strip()
        # username@domain
        valid_email=re.search(r"^[a-zA-Z][a-zA-Z0-9_-]*@([a-zA-Z]+\.)*[a-zA-Z]+$", email_str)
        if valid_email is None:
            logging.info("Invalid Email String.")
            otp_msg_placeholder.info("Invalid Email")
            return False, None
        else:
            logging.info("Email Validated Successfully.")
            otp_msg_placeholder.info("Sending OTP...")
            return True, valid_email.string


## Send mail func
def send_mail(mail_str, otp_msg_placeholder):
    
    logging.info("Mailing Process Started.")
    logging.info("Generating OTP")
    otp=generate_otp()

    try:
        # Setting and Starting Server
        logging.info("Starting Server.")
        server=smtplib.SMTP(host=settings.get('host'),port=settings.get('port'))
        server.starttls()

        # Login into account
        logging.info("Logging into host account.")
        sender_email=settings.get('sender_email')
        pwd=settings.get('passkey')
        server.login(user=sender_email,password=pwd)
        
        message = EmailMessage()
        message.add_header("To", mail_str)
        message.add_header("Subject", "OTP Code")
        
        body=f'''      Hi,\n      Your OTP is {otp}.'''
        message.set_content(body)
        message_as_bytes = message.as_bytes()

        # Sending email
        logging.info("Sending Mail.")
        senderrors = server.sendmail(from_addr=sender_email, to_addrs=mail_str, msg=message_as_bytes)
        server.quit()

        # verifying email delivery
        email_delivered, msg_info = got_any_reply(for_otp=otp)

        if email_delivered is not None and email_delivered and len(senderrors) == 0:
            otp_msg_placeholder.success(msg_info)
            logging.info("Email send successfully.")
            return otp
        else:
            otp_msg_placeholder.info(msg_info)
            logging.info("May be username, domain or mailing related issue.")
            return 0

    except Exception as e:
        logging.info(f"Email Exception : {str(e)}.")
        otp_msg_placeholder.info("Invalid email or connection issue.")
        return 0



# checking if any reply to 'mail_id'
def got_any_reply(for_otp):
    server ="imap.gmail.com"					 
    imap = imaplib.IMAP4_SSL(server)

    username =settings.get('sender_email') 
    password =settings.get('passkey')

    imap.login(username, password)			 

    try:
        res, messages = imap.select('"[Gmail]/Sent Mail"')
        res, msg_no_list = imap.search(None, f'(BODY "Your OTP is {for_otp}.")')
        # msg_no = decode(msg_no_list[0])[0]
        msg_no = msg_no_list[0].decode("utf-8")

        if len(msg_no_list) == 1:
            res, msg = imap.fetch(msg_no, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    msg_id = msg["Message-ID"]

                    if msg_id is not None:
                        res, messages = imap.select()
                        res, msg_no_list = imap.search(None, f'(HEADER "In-Reply-To" "{msg_id}")')
                        # msg_no = decode(msg_no_list[0])[0]
                        msg_no = msg_no_list[0].decode("utf-8")

                        imap.close()
                        imap.logout()

                        if len(msg_no) == 0:
                            return True, "OTP Send Successfully"
                        else:
                            return False, "Invalid Email"
                    else:
                        return None, "Email Issue, Try Again!"
        else:
            imap.close()
            imap.logout()
            return None, "Email Not Send, Try Again!"
        
    except Exception as e:
        imap.close()
        imap.logout()
        logging.info(f"Exception in get_mail_id : {str(e)}")
