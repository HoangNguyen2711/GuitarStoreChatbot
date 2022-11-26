
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


class Coupon(Action):

    # def name(self) -> Text:
    #     return "action_coupon"

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("SELECT name, vale, expery_date FROM coupons")
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            print("Chúng mình đang có các mã giảm giá sau đây ạ: ")
            for x in myresult:
                print(x[0]+ ' -$' + str(int(x[1]))+' Ngày hết hạn: ' +str(x[2]))
        else:
            print("Dạ hiện tại chúng mình không có chương trình khuyến mãi nào ạ")