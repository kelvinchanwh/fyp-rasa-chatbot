

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import EventVerbosity

import logging
logger = logging.getLogger(__name__)

import requests
import json

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted

from bs4 import BeautifulSoup
import urllib.request
import re
import requests

class SaveOrigin(Action):
    def name(self):
        return 'action_save_origin'

    def run(self, dispatcher, tracker, domain):
        orig = next(tracker.get_latest_entity_values("location"), None)
        if not orig:
            dispatcher.utter_message("Please enter a valid airport code")
            return [UserUtteranceReverted()]
        return [SlotSet('from',orig)]
    
class SaveDestination(Action):
    def name(self):
        return 'action_save_destination'

    def run(self, dispatcher, tracker, domain):
        dest = next(tracker.get_latest_entity_values("location"), None)
        if not dest:
            dispatcher.utter_message("Please enter a valid airport code")
            return [UserUtteranceReverted()]
        return [SlotSet('to',dest)]

class SaveDate(Action):
    def name(self):
        return 'action_save_date'

    def run(self, dispatcher, tracker, domain):
        inp = next(tracker.get_latest_entity_values("date"), None)
        if not inp:
            dispatcher.utter_message("Please enter a valid date")
            return [UserUtteranceReverted()]
        return [SlotSet('date',inp)]

class ActionSlotReset(Action): 	
    def name(self): 
        return 'action_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 
        return[AllSlotsReset()]

class getFlightStatus(Action):
    def name(self):
        return 'action_get_flight'
    def run(self, dispatcher, tracker, domain):
        orig=tracker.get_slot('from')
        dest=tracker.get_slot('to')
        dat=tracker.get_slot('date')
        dispatcher.utter_message("Here is the link to your flight booking")
        urls = ("https://api.skypicker.com/flights?"+
                       "flyFrom=" + orig +
                       "&to="+ dest +
                       "&dateFrom=" + dat + 
                       "&partner=picky") 
        response = requests.get(urls)
        data = response.text
        parsed = json.loads(data) 
        class Test(object):
            def __init__(self, data):
                self.__dict__ = json.loads(data)
        flight_data = Test(data)
        flight_data = flight_data.data[1]['deep_link']
        dispatcher.utter_message(flight_data)
        return []
