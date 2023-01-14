
from application.workers import celery
from datetime import datetime
from application.database import db
from application.models import *
import csv


@celery.task()
def exportList(user_id):
    print("hello")
    # save csv file
    user = User.query.filter_by(id=user_id).first()
    lists = user.lists
    print(lists)
    header = ["list_id","name","description"]
    f = open("list.csv",'w')
    # with open('./lists.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     for list in lists:
    #         li = [list.id,list.name, list.description]
    #         print(li)
    #         writer.writerow(li)
    return 200