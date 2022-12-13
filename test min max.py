from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
from rasa_sdk.events import SlotSet

import requests
import mariadb
import urllib.request


mydb = mariadb.connect(
    host="localhost",
    user="root",
    password="",
    database="guitarstoree"
)


class PriceMin(Action):

    cur = mydb.cursor()
    cur.execute("Select name, price, sale from products order by price asc limit 1")
    myresult = cur.fetchall()
 
    print(
        "Dạ đây là sản phẩm giá thấp nhất của chúng mình ạ: ")
    for x in myresult:
        print((x[0])+' giá: $'+str(x[2])+', đang giảm: '+str(int(x[1]))+'%')
