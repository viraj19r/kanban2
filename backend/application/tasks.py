from application.workers import celery
from application.database import db
from application.models import *
import csv,time
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from celery.schedules import crontab
from email import encoders
# no of incomplete task
import os
from weasyprint import HTML

@celery.on_after_finalize.connect
def dailyRemindScheduler(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=20,minute=30),sendDailyReminder.s(),name="sending daily mail")
    sender.add_periodic_task(crontab(day_of_month=1,hour=10,minute=10),sendMonthlyReminder.s(),name="sending monthly mail")

# @celery.on_after_finalize.connect
# def monthlyRemindScheduler(sender, **kwargs):
#     sender.add_periodic_task(crontab(day_of_month=13,hour=16,minute=34),sendMonthlyReminder.s(),name="sending mail")



@celery.task()
def sendMonthlyReminder():
    users = User.query.all()
    listCount = 0
    cardCount = 0
    pendingCards = 0
    completedCards = 0
    path = os.getcwd()
    for user in users:
        for list in user.lists:
            listCount += 1
            for card in list.cards:
                cardCount += 1
                if not card.completed_status:
                    pendingCards += 1
                else:
                    completedCards += 1
        
        with open(path+"/templates/monthly_rem.html") as f:
            template = Template(f.read())
            file1 = template.render(fname = user.fname, lname=user.lname, pending_task = pendingCards, completedCards=completedCards, listCount=listCount,cardCount=cardCount)

        pdf_render = HTML(string=file1)
        pdf = pdf_render.write_pdf(path+"/templates/monthly.pdf")
        sendMail(user.email, 'abc@kanban.com', "Monthly Reminder for Uncompleted Cards",f'Hii {user.fname}, Attached is your montly report',path+"/templates/monthly.pdf" )

@celery.task()
def sendDailyReminder():
    users = User.query.all()
    pendingCards = 0
    path = os.getcwd()
    for user in users:
        for list in user.lists:
            for card in list.cards:
                if not card.completed_status:
                    pendingCards += 1
        
        with open(path+"/templates/daily_rem.html") as f:
            template = Template(f.read())
            file1 = template.render(user = user.fname, pending_task = pendingCards)
        sendMail(user.email, 'abc@kanban.com', "Daily Reminder for Uncompleted Cards", file1)


@celery.task()
def sendMail(to,mailfrom, subject,message, attachment=False):
    text = MIMEMultipart()
    text['From'] = mailfrom
    text['To'] = to
    text['Subject'] = subject
    text.attach(MIMEText(message,'html'))   
    if attachment:
        with open(attachment,'rb') as attachment:
            file = MIMEBase('application','octet-stream')
            file.set_payload(attachment.read())
            encoders.encode_base64(file)
            file.add_header('Content-Disposition','attachment; filename=monthly.pdf')
            text.attach(file)

            
    email_sender = smtplib.SMTP(host='localhost',port=1025)
    email_sender.login(mailfrom,'12345')
    email_sender.send_message(text)
    email_sender.quit()
    return 200








@celery.task()
def exportBoard(user_id):
    # save csv file
    user = User.query.filter_by(id=user_id).first()
    lists = user.lists
    header = ["list_id","name","description",'completed_cards','incomplete_cards']
    with open('static/board{}.csv'.format(user_id), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for list in lists:
            cards = list.cards
            complete = 0
            incomplete = 0
            for card in cards:
                if card.completed_status:
                    complete += 1
                else:
                    incomplete += 1
            li = [list.id,list.name, list.description,complete,incomplete]
            writer.writerow(li)
    return 200


@celery.task()
def exportList(list_id):
    # save csv file 
    list = List.query.filter_by(id=list_id).first()
    cards = list.cards
    header = ['card_id','title','content','deadline','date_created','completed_status','date_completed']
    with open('static/list{}.csv'.format(list_id), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for card in cards:
            li = [card.id,card.title, card.content,card.deadline,card.date_created,card.completed_status,card.date_completed]
            writer.writerow(li)
    return 200