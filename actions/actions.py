# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

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

class Hello(Action):

    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello There!")

        return []

class weather(Action):
    def name(self) -> Text:
        return "action_weather"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en'}
        city= 'vinhlong'
        city = city+'+weather'
        res = requests.get(f'https://www.google.com/search?q={city}&source=hp&ei=m9FoY9OeN5X6hwPOp4foCw&iflsig=AJiK0e8AAAAAY2jfq4ljjsXUXSHyFGtYeAohoPIzZK95&ved=0ahUKEwiT2ITD4pv7AhUV_WEKHc7TAb0Q4dUDCAg&uact=5&oq=cantho&gs_lp=Egdnd3Mtd2l6uAED-AEBMgcQLhiABBgKMgsQLhiABBjHARivATILEC4YgAQYxwEYrwEyDRAuGIAEGMcBGK8BGAoyBRAAGIAEMgcQLhiABBgKMgsQLhiABBjHARivATIFEAAYgAQyBRAAGIAEMgUQABiABMICCBAAGLEDGIMBwgIIEC4YsQMYgwHCAgUQLhiABMICBRAAGLEDwgIKEC4YgAQY1AIYCqgCAEjgClCXAliOB3ABeADIAQCQAQCYAcwBoAHSBqoBBTAuNS4x&sclient=gws-wiz', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        dispatcher.utter_message(location)
        dispatcher.utter_message(info + ' v??o l??c: '+ time.lower())
        dispatcher.utter_message('Nhi???t ????? trung b??nh: '+weather+"??C")

class news(Action):

    def name(self) -> Text:
        return "action_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            url =  'https://guitar.com/news/'

            page = urllib.request.urlopen(url)

            soup = BeautifulSoup(page, 'html.parser')
            new_feeds = soup.find('h3',class_='entry-title td-module-title').find_all('a')
            for feed in new_feeds:
                title = feed.get('title')
                link = feed.get('href')
                dispatcher.utter_message('Tin m???i nh???t t??? guitar.com ????y ???: {} - Link: {}'.format(title, link))


class Coupon(Action):

    def name(self) -> Text:
        return "action_coupon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("SELECT name, vale, expery_date FROM coupons")
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            dispatcher.utter_message("Ch??ng m??nh ??ang c?? c??c m?? gi???m gi?? sau ????y, v?? kh??ng ??p d???ng khuy???n m??i ch???ng ???: ")
            for x in myresult:
                dispatcher.utter_message(x[0]+ ' -$' + str(int(x[1]))+' Ng??y h???t h???n: ' +str(x[2]))
        else:
            dispatcher.utter_message("D??? hi???n t???i ch??ng m??nh kh??ng c?? ch????ng tr??nh khuy???n m??i n??o ???")

def listToString(s):
   
    str1 = " "
   
    return (str1.join(s))

class Category(Action):

    def name(self) -> Text:
        return "action_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("SELECT name FROM categories WHERE parent_id is not null")
        myresult = cur.fetchall()

        dispatcher.utter_message("D??? ch??ng m??nh c?? c??c danh m???c s???n ph???m sau ???: ")
        for x in myresult:
            dispatcher.utter_message(listToString(x))

class HotItems(Action):

    def name(self) -> Text:
        return "action_hotitems"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("select pd.id, pd.name, sum(od.quantity) as quantity from order_details od join products pd on od.product_id = pd.id group by pd.id, pd.name order by quantity desc limit 3")
        myresult = cur.fetchall()


        dispatcher.utter_message("D??? ????y l?? top 3 s???n ph???m b??n ch???y nh???t c???a ch??ng m??nh ???: ")
        for x in myresult:
            dispatcher.utter_message((x[1]))

class HotSale(Action):

    def name(self) -> Text:
        return "action_hotsale"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("select name, sale from products order by sale desc limit 5")
        myresult = cur.fetchall()

        dispatcher.utter_message("D??? ????y l?? top 5 s???n ph???m gi???m gi?? l???n nh???t c???a ch??ng m??nh ???: ")
        for x in myresult:
            dispatcher.utter_message((x[0])+', ??ang gi???m: '+str(int(x[1]))+'%')

class ProductDetail(Action):

    def name(self) -> Text:
        return "action_product_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot("product_detail")
        cur = mydb.cursor()
        sql='SELECT name, price, sale FROM products WHERE name LIKE %s'
        args=['%'+str(product_name)+'%']
        cur.execute(sql,args)
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            dispatcher.utter_message("D??? ch??ng m??nh c?? c??c s???n ph???m sau ????y: ")
            for x in myresult:
                dispatcher.utter_message(x[0]+', gi??: $'+str(x[1])+', ??ang gi???m: '+str(x[2])+'%')
        else:
            dispatcher.utter_message("D??? ch??ng m??nh kh??ng c?? s???n ph???m ???? ??? :(")

class PriceMinMax(Action):

    def name(self) -> Text:
        return "action_sort_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pricemin = tracker.get_slot("price_min")
        pricemax = tracker.get_slot("price_max")
        cur = mydb.cursor()
        sql='SELECT name, price, sale FROM products WHERE price between %s and %s'
        args1=pricemin
        args2=pricemax
        cur.execute(sql,(args1, args2))
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            dispatcher.utter_message("D??? ch??ng m??nh c?? c??c s???n ph???m sau ????y: ")
            for x in myresult:
                dispatcher.utter_message(x[0]+', gi??: $'+str(x[1])+', ??ang gi???m: '+str(x[2])+'%')
        else:
            dispatcher.utter_message("D??? ch??ng m??nh kh??ng c?? s???n ph???m trong t???m gi?? ???? ??? :(")


class PriceMin(Action):

    def name(self) -> Text:
        return "action_price_min"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = mydb.cursor()
        cur.execute("Select name, sale, price from products order by price asc limit 1")
        myresult = cur.fetchall()
 
        dispatcher.utter_message(
        "D??? ????y l?? s???n ph???m gi?? th???p nh???t c???a ch??ng m??nh ???: ")

        for x in myresult:
         dispatcher.utter_message(str(x[0])+' gi??: $'+str(x[2])+', ??ang gi???m: '+str(int(x[1]))+'%')

class PriceMax(Action):

    def name(self) -> Text:
        return "action_price_max"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = mydb.cursor()
        cur.execute("Select name, sale, price from products order by price desc limit 1")
        myresult = cur.fetchall()
 
        dispatcher.utter_message(
        "D??? ????y l?? s???n ph???m gi?? cao nh???t c???a ch??ng m??nh ???: ")

        for x in myresult:
         dispatcher.utter_message(str(x[0])+' gi??: $'+str(x[2])+', ??ang gi???m: '+str(int(x[1]))+'%')
