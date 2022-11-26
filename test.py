from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
from rasa_sdk.events import SlotSet

import requests
import mariadb
import urllib.request 

    
mydb =  mariadb.connect(
  host="localhost",
  user="root",
  password="",
  database="guitarstoree"
)

class PriceMinMax(Action):

    # def name(self) -> Text:
    #     return "action_sort_price"

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pricemin = "100"
        pricemax = "1000"
        cur = mydb.cursor()

        sql='SELECT name, price FROM products WHERE price between %s and %s'
        args1=pricemin
        args2=pricemax
        cur.execute(sql,(args1, args2))
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            print("Dạ chúng mình có các sản phẩm sau đây: ")
            for x in myresult:
                print(x[0]+' giá: $'+str(x[1]))
        else:
            print("Dạ chúng mình không có sản phẩm đó ạ :(")
