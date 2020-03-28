# Marakulin Andrey @annndruha
# 2020
import json
import time
import traceback

import psycopg2

import vk_func as vk
from . import config

# Pages of keyboard menu:
def main_page(user_id, ans='Главное меню', attach = None):
    kb = vk.VkKeyboard(one_time=False)
    kb.add_button('Перейти на сайт печати', color='primary', payload = ["command","site"])
    kb.add_line()
    kb.add_button('Информация', color='primary', payload = ["command","info"])
    kb.add_line()
    kb.add_button('Обновить данные о себе', color='primary', payload = ["command","info"])
    kb.add_line()
    kb.add_button('Загрузить PDF-файл', color='positive', payload = ["next_page","load_page"])
    vk.send_keyboard(user_id, kb.get_keyboard(), ans, attach=attach)

def load_page(user_id, ans='Проверьте актуальность настроек и просто отправьте мне файл'):
    kb = vk.VkKeyboard(one_time=False)
    if True: # Check user autorization
        #
        # Load user setting from server
        # Change buttons colors
        kb.add_button('Цветная', color='primary', payload = ["command","to_color"])
        kb.add_button('Чёрно-белая', color='default', payload = ["command","to_white_black"])
        kb.add_line()
        kb.add_button('Отмена', color='default', payload = ["command","cancel"])

    elif auto_user_detect():
        #
        #
        #
        #
        pass
    else:
        ans = 'Сначала необходимо подтвердить вашу личность.\n Вы являетесь членом профсоюза?'
        kb.add_button('Да', color='positive', payload = ["command","ismember"])
        kb.add_button('Нет', color='negative', payload = ["command","notmember"])
        kb.add_line()
        kb.add_button('Отмена', color='default', payload = ["command","cancel"])

    vk.send_keyboard(user_id, kb.get_keyboard(), ans, attach=attach)




# Browsing between keybord pages
def keyboard_browser(user_id, str_payload):
    try:
        payload = json.loads(str_payload)
        if not isinstance(payload, list):
            ans = 'Здравствуйте, Вас приветствует принтер-бот физического факультета МГУ! С помощью меня вы можете печатать файлы в профкоме!'
            main_page(user_id, ans)
        elif payload[0] == 'command':
            if payload[1] == 'cancel':
                main_page(user_id)
            elif payload[1] == 'site':
                ans = 'http://printer.profcomff.com'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'info':
                ans = 'Принтер-бот физического факультета @2020'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'to_color':
                ans = 'Тип печати изменён на цветуню.'
                # change in db
                load_page(user_id, ans)
            elif payload[1] == 'to_white_black':
                ans = 'Тип печати изменён на чёрно-белую.'
                # change in db
                load_page(user_id, ans)
            elif payload[1] == 'ismember':
                ans = 'Отправьте мне текстовое сообщение с фамилией и номером профсоюзного билета в формате:'
                vk.send_msg(user_id, ans)
                time.sleep(0.5)
                ans = 'Фамилия\n1234567'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'notmember':
                ans = 'Отправьте мне текстовое сообщение с фамилией, номером студенческого билета и номером курса в формате:'
                vk.send_msg(user_id, ans)
                time.sleep(0.5)
                ans = 'Фамилия\n01234567\n1'
                vk.send_msg(user_id, ans)

        elif payload[0] == 'next_page':
            if payload[1] == 'load_page':
                load_page(user_id)

    except psycopg2.Error as err:
        ans = 'К сожалению, сервис временно недоступен.'
        vk.send_msg(user_id, ans)
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Database Error (keyboard_browser), raise:", time.gmtime()))
    except OSError as err:
        raise err
    except BaseException as err:
        ans = dict.errors['kb_error']
        vk.send_msg(user_id, ans)
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (keyboard_browser), description:", time.gmtime()))
        traceback.print_tb(err.__traceback__)
        print(str(err.args))