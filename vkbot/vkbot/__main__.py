import logging
import os
from VKLongPollAPI import VKLongPollAPI

logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG
)

def event_type_logger(event):
    print(event['type'])
    return None

def message_body_logger(event):
    print(event['object']['body'])
    return None

if __name__ == "__main__":
    lpa = VKLongPollAPI(os.getenv('VK_GROUP_ID'),os.getenv('VK_GROUP_SECRET'))
    lpa.add_listener(None, event_type_logger)
    lpa.add_listener('message_new', message_body_logger)
    lpa.start()
    lpa.join()