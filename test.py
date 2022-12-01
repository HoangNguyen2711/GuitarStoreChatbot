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


class ProductDetail(Action):

    cur = mydb.cursor()
    cur.execute("select name, sale from products order by sale desc limit 5")
    myresult = cur.fetchall()

    print(myresult)
    # print(
    #     "Dạ đây là top 3 sản phẩm hot của chúng mình ạ: ")
    # for x in myresult:
    #     print((x[1]))
