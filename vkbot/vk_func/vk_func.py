# Marakulin Andrey @annndruha
# 2020
import time
import datetime
import traceback
import requests
import json

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

import config

vk = VkApi(token=config.access_token) # Auth with community token
longpoll = VkLongPoll(vk) # Create a longpull variable

def reconnect():
    global vk
    global longpoll
    vk = VkApi(token=config.access_token)
    longpoll = VkLongPoll(vk)

def user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def send_msg(user_id, message=None, attach=None, parse_links = False):
    params = {'user_id': user_id, 'random_id': get_random_id()}
    if message is not None and attach is not None:
        params['message']=message
        params['attachment']=attach
    elif message is not None and attach is None:
        params['message']=message
    elif message is None and attach is not None:
        params['attachment']=attach
    if parse_links == False:
        params['dont_parse_links']=1
    vk.method('messages.send', params)

def send_keyboard(user_id, kb, message, attach = None):
    if attach==None:
        vk.method('messages.send', {'user_id': user_id, 'keyboard': kb, 'message': message, 'random_id': get_random_id()})
    else:
        vk.method('messages.send', {'user_id': user_id, 'keyboard': kb, 'message': message, 'attachment':attach,'random_id': get_random_id()})

def get_doc(user_id, file_dir):
    pass
def upload_doc_to_server():
    pass