# Marakulin Andrey @annndruha
# 2020
import json
import time
import traceback

import psycopg2

import vk_func as vk
from . import config

# Pages of keyboard menu:
def main_page(user_id, ans='������� ����', attach = None):
    kb = vk.VkKeyboard(one_time=False)
    kb.add_button('������� �� ���� ������', color='primary', payload = ["command","site"])
    kb.add_line()
    kb.add_button('����������', color='primary', payload = ["command","info"])
    kb.add_line()
    kb.add_button('�������� ������ � ����', color='primary', payload = ["command","info"])
    kb.add_line()
    kb.add_button('��������� PDF-����', color='positive', payload = ["next_page","load_page"])
    vk.send_keyboard(user_id, kb.get_keyboard(), ans, attach=attach)

def load_page(user_id, ans='��������� ������������ �������� � ������ ��������� ��� ����'):
    kb = vk.VkKeyboard(one_time=False)
    if True: # Check user autorization
        #
        # Load user setting from server
        # Change buttons colors
        kb.add_button('�������', color='primary', payload = ["command","to_color"])
        kb.add_button('׸���-�����', color='default', payload = ["command","to_white_black"])
        kb.add_line()
        kb.add_button('������', color='default', payload = ["command","cancel"])

    elif auto_user_detect():
        #
        #
        #
        #
        pass
    else:
        ans = '������� ���������� ����������� ���� ��������.\n �� ��������� ������ ���������?'
        kb.add_button('��', color='positive', payload = ["command","ismember"])
        kb.add_button('���', color='negative', payload = ["command","notmember"])
        kb.add_line()
        kb.add_button('������', color='default', payload = ["command","cancel"])

    vk.send_keyboard(user_id, kb.get_keyboard(), ans, attach=attach)




# Browsing between keybord pages
def keyboard_browser(user_id, str_payload):
    try:
        payload = json.loads(str_payload)
        if not isinstance(payload, list):
            ans = '������������, ��� ������������ �������-��� ����������� ���������� ���! � ������� ���� �� ������ �������� ����� � ��������!'
            main_page(user_id, ans)
        elif payload[0] == 'command':
            if payload[1] == 'cancel':
                main_page(user_id)
            elif payload[1] == 'site':
                ans = 'http://printer.profcomff.com'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'info':
                ans = '�������-��� ����������� ���������� @2020'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'to_color':
                ans = '��� ������ ������ �� �������.'
                # change in db
                load_page(user_id, ans)
            elif payload[1] == 'to_white_black':
                ans = '��� ������ ������ �� �����-�����.'
                # change in db
                load_page(user_id, ans)
            elif payload[1] == 'ismember':
                ans = '��������� ��� ��������� ��������� � �������� � ������� ������������ ������ � �������:'
                vk.send_msg(user_id, ans)
                time.sleep(0.5)
                ans = '�������\n1234567'
                vk.send_msg(user_id, ans)
            elif payload[1] == 'notmember':
                ans = '��������� ��� ��������� ��������� � ��������, ������� ������������� ������ � ������� ����� � �������:'
                vk.send_msg(user_id, ans)
                time.sleep(0.5)
                ans = '�������\n01234567\n1'
                vk.send_msg(user_id, ans)

        elif payload[0] == 'next_page':
            if payload[1] == 'load_page':
                load_page(user_id)

    except psycopg2.Error as err:
        ans = '� ���������, ������ �������� ����������.'
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