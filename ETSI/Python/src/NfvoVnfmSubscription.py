import time
import json
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class NfvoVnfmSubscription(BaseApi):

    SUBSCRIPTION_URL = 'admin/server'

    STATUS = {"NOT_STARTED": False,
              "REMOVED": False,
              "STARTED": False,
              "SUCCESS": True,
              "FAILED": True,
              }

    def subscribe(self, _payload):
        _url = self.SUBSCRIPTION_URL
        response = self.do_post(_url, _payload)
        return response

    def subscribe_get_status(self, server_id):
        _url = self.SUBSCRIPTION_URL
        response = self.do_get(_url)
        
        subscription = ''
        for index, item in enumerate(response.json()):
            item_server_id = item['id']
            if item_server_id == server_id:
                subscription = item
                break
        return subscription

    def subscribe_completion_wait(self, server_id, timeout=60):
        subscription = self.subscribe_get_status(server_id)
        state = subscription['serverStatus']

        while (timeout > 0):
            subscription = self.subscribe_get_status(server_id)
            state = subscription['serverStatus']
            timeout -= 1
            time.sleep(1)
            if self.STATUS.get(state):
                break
            else:
                continue

        return subscription 
