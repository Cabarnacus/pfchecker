#! /usr/local/bin/python3.8

from datetime import datetime
from time import sleep
from tabulate import tabulate
import os, smtplib, ssl #,random

GATEWAY = "LTEGW"
POLL_FREQ = 5
NUM_OF_METRICS = 15

port = 587  # For starttls
smtp_server = "smtp.office365.com"
login_email = "xxx@email.com"
sender_email = "xxy@email.com"
receiver_email = "xxz@email.com"
password = "password"
email_flag = False

ping_lst = []
loss_lst = []


def gateway_status():

    # gateway can be 'online', 'down' on [6]. 'none', 'force_down' 'delay', 'highdelay' 'loss' 'highloss' on [7]

    stream = os.popen(f'pfSsh.php playback gatewaystatus | grep {GATEWAY}')
    output = stream.read().strip().split()
    status = output[6]
    substatus = output[7]
    ping = output[3]
    loss = output[5]

    return status, substatus, ping, loss


# def dummy():

#     status = "down" #random.choice(["online", "down"])
#     substatus = "highloss" #random.choice(["none", "delay", "highdelay", "loss", "highloss"])
#     ping = "700.1ms" #round(random.uniform(50, 80), 2)
#     loss = "100%"

#     return status, substatus, ping, loss


def send_mail(status, substatus, ping_lst=[], loss_lst=[]):

    now = datetime.now()
    str_now = now.strftime("%d/%m/%Y %H:%M:%S")
    table = zip(reversed(ping_lst), reversed(loss_lst))
    metrics = tabulate(table, headers=["Ping", "Loss"], tablefmt="simple")

    if status == "down":
        SUBJECT = f"{GATEWAY} Gateway Down - '{substatus}'"
        TEXT = f"{GATEWAY} Gateway was detected 'down' - '{substatus}' at {str_now}.\n\nLatest metrics as follows (most recent first):\n\n{metrics}"

    elif status == "online":
        SUBJECT = f"{GATEWAY} Gateway Restored"
        TEXT = f"{GATEWAY} Gateway back 'online' - '{substatus}' at {str_now}.\n\nLatest metrics as follows (most recent first):\n\n{metrics}"

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(login_email, password)
        server.sendmail(sender_email, receiver_email, message)    


while True:

    status, substatus, ping, loss = gateway_status()

    if len(ping_lst) < NUM_OF_METRICS:
        ping_lst.append(ping)
        loss_lst.append(loss)

    else:
        ping_lst.pop(0)
        loss_lst.pop(0)

        ping_lst.append(ping)
        loss_lst.append(loss)   


    if status == "down":
        if email_flag != True:
            try:
                send_mail(status, substatus, ping_lst, loss_lst)
                email_flag = True
            except:
                pass    

    elif status == "online":
        if email_flag != False:
            try:    
                send_mail(status, substatus, ping_lst, loss_lst)
                email_flag = False
            except:
                pass

    sleep(POLL_FREQ)