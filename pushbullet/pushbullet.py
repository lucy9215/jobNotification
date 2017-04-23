#!/root/miniconda3/bin/python
# -*- coding: utf-8 -*-
#    
#    API Auther Github Page: https://github.com/Azelphur/pyPushBullet 

import json
import requests
from requests.auth import HTTPBasicAuth
from websocket import create_connection
from .userSettings import *
import logging

class PushBullet():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def _request(self, method, url, postdata=None, params=None, files=None):
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "User-Agent": "LucyAI"}

        if postdata:
            postdata = json.dumps(postdata)

        r = requests.request(method,
                             url,
                             data=postdata,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.apiKey, ""),
                             proxies=PROXIES)

        r.raise_for_status()
        return r.json()

    def getDevices(self):
        """ Get devices
            https://docs.pushbullet.com/v2/devices

            Get a list of devices, and data about them.
        """

        return self._request("GET", HOST + "/devices")["devices"]

    def pushNote(self, recipient, title, body, recipient_type="device_iden"):
        """ Push a note
            https://docs.pushbullet.com/v2/pushes

            Arguments:
            recipient -- a recipient
            title -- a title for the note
            body -- the body of the note
            recipient_type -- a type of recipient (device, email, channel or client)
        """

        data = {"type": "note",
                "title": title,
                "body": body}

        data[recipient_type] = recipient

        return self._request("POST", HOST + "/pushes", data)

def print_devices(devices):
    for d in devices:
        if d['pushable']:
            print ('Pushable device:%s, active:%s, device iden:%s'%(d['nickname'], d['active'], d['iden']))
            logging.info('Pushable device:%s, active:%s, device iden:%s'%(d['nickname'], d['active'], d['iden']))

def main():
    apiKey = USER_API_KEY #"YOUR_API_KEY_HERE"
    p = PushBullet(apiKey)

    try:
        # Get a list of devices
        devices = p.getDevices()
        # print_devices(devices)
    except:
        print('You may have a network connection probelem to connect pushbullet.com.')
    else:
        if len(devices)!=0:
            print_devices(devices)
        #  Send a note
        p.pushNote(USER_DEVICE_IDEN, 'Hi! I AM ALIVE!!', 'Lucy AI sends greetings!')


if __name__ == '__main__':
    main()
