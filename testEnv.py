#!/root/miniconda3/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
from pushbullet.messenger import Messenger

FORMAT = '[%(asctime)-15s] @%(levelname)-7s ->%(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT,filename='M_run.log',filemode='w')

def test_messenger(filename):
    M = Messenger()
    M.test()
    with open(filename,'r') as f: 
        for line in f.readlines():
            M.message_buffer(line)
    # M.send_all()    
    M.test("Nothing New. :)")

def test_env():

    M = Messenger()
    M.test()
    # for line in sys.stdin:
        # M.message_buffer(line)
    # M.send_all()    
    # M.test("Nothing New. :)")

if __name__ == '__main__':
    test_env()
#    test_messenger('./backup/bb.log')
