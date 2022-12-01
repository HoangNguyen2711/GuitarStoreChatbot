from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
from rasa_sdk.events import SlotSet

import requests
import mariadb
import urllib.request


class news(Action):

    # def name(self) -> Text:
    #     return "action_news"

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = 'http://127.0.0.1:8000/'

        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')
        new_feeds = soup.find(
            'h3', class_='entry-title td-module-title').find_all('a')
        for feed in new_feeds:
            title = feed.get('title')
            link = feed.get('href')
            print(
                'Tin mới nhất từ guitar.com đây ạ: {} - Link: {}'.format(title, link))
