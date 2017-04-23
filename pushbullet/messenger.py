#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import logging
from .pushbullet import *

class Messenger(object):
    """docstring for Message"""
    def __init__(self): #, arg):
        # super(Message, self).__init__()
        # self.arg = arg
        self.ready = False
        self.message = ''
        self.error_bag = ''
        self.result_bag = ''
        self.pattern_time=re.compile(r'\d{1,2}h:\d{1,2}m:\d{1,2}s:\d{1,4}ms')
        self.pattern_process = re.compile(r'\([0-9\ ]{0,2}/\w{2}\)')
        self.pattern_stream = re.compile(r'stream\s+\d{1,2}')
        self.pattern_long_space = re.compile(r'\s+')
    def _message_chopper(self,line):
        if 'Finished' in line:
                return line
        else:
            return 
    def bb_message_chopper(self,line):
        if 'Load test' in line:
            if 'finished' in line:
                try:
                    time = re.search(self.pattern_time,line)[0]
                except:
                    logging.info('re seach time failed')
                    time = 'TIME SEARH FAILED'
                message = 'Load finished. Time: '+time
                return message
        elif 'Power test' in line:
            if 'finished' in line:
                try:
                    time = re.search(self.pattern_time,line)[0]
                except:
                    time = ' TIME SEARH FAILED '
                try:
                    process = re.search(self.pattern_process,line)[0]
                except:
                    if time:
                        process = ' finished.'
                    else:
                        process = ' PROCESS SEARCH FAILED '
                    # logging.info('re seach time failed')
                message = 'Power'+process+' Time: '+time
                if process == ' finished.':
                    return message
        elif 'throughput' in line:
            if 'finished' in line:
                try:
                    self.pattern_long_space = re.compile(r'\s+')
                    stream_buff = re.search(self.pattern_stream,line)[0]
                    stream = self.pattern_long_space.sub(' ',stream_buff)
                except :
                    stream =''
                try:
                    time = re.search(self.pattern_time,line)[0]
                except:
                    time = ' TIME SEARH FAILED '
                try:
                    process = re.search(self.pattern_process,line)[0]
                except:
                    if time:
                        process = ' finished.'
                    else:
                        process = ' PROCESS SEARCH FAILED '
                    # logging.info('re seach time failed')
                message = 'Throughput '+ stream +process+' Time: '+time
                # if stream == 'stream 0':
                if process == ' finished.':
                    return message
        elif 'benchmark: Stop' in line:
            if 'finished' in line:
                try:
                    time = re.search(self.pattern_time,line)[0]
                except:
                    time = ' TIME SEARH FAILED '
                message = 'Benchmark Stop. '+'Time: '+time
                return message
        elif 'VALID BBQpm' in line:
            self.result_bag+=line
            message = line[:-1]
            return message
        elif 'Benchmark run terminated' in line:
            self.error_bag+=line
        elif 'Reason:' in line:
            self.error_bag+=line
        elif 'No final result available.' in line:
            self.error_bag+=line
            message=self.error_bag
            return message
    def message_buffer(self, line):
        if line[-1] == '\n':
            line_tmp=line[:-1]
        else:
            line_tmp=line
        print(line_tmp)
        sys.stdout.flush()
        logging.info(line_tmp)        
        if line!='':
            message2push=self.bb_message_chopper(line)
        if message2push:
            self.message+=message2push
            self.ready=True
        if self.ready == True:
            logging.info('Pushing message...(%s)'%self.message)
            self.send()
    def test(self,message='Your network seems good.'):
        p = PushBullet(USER_API_KEY)
        try:
            # Get a list of devices
            devices = p.getDevices()
            # print_devices(devices)
        except:
            print('You may have a network connection probelem to connect pushbullet.com.')
            sys.stdout.flush()
            logging.info('You may have a network connection probelem to connect pushbullet.com.')
        else:
            if len(devices)!=0:
                print_devices(devices)
                sys.stdout.flush()
            #  Send a note
            p.pushNote(USER_DEVICE_IDEN, 'Alfred is with you.', message)
    def send(self):
        p = PushBullet(USER_API_KEY)
        try:
            # Get a list of devices
            devices = p.getDevices()
            # devices = 'pass'
            # print_devices(devices)
        except:
            print('You may have a network connection probelem to connect pushbullet.com.')
            sys.stdout.flush()
            logging.info('You may have a network connection probelem to connect pushbullet.com.')
        else:
            if len(devices)!=0:
                #  Send a note
                p.pushNote(USER_DEVICE_IDEN, 'News from Alfred', self.message)
                # print('PUSHING NEWS:%s'%self.message)
                self.message=''
                self.ready=False
    def send_all(self,retry=20):
        while retry>0 and self.message!='':
            M.send()
            retry-=1
            logging.info('Remaining Attempts:%d'%retry)