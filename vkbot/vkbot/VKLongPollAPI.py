import os
import requests
import logging
from enum import Enum
from multiprocessing import Manager, Process, current_process

class VKLongPollAPI(Process):
    """Класс для обработки сообщений через long poll с подключением к VK API

    В бесконечном цикле делает запрос к LongPoll VK API и обрабатывает ответ 
    пользовательскими Listener'ами.
    """
    base_api_url = 'https://api.vk.com/method/'

    def __init__(self, group_id, access_token=None, *, lp_timewait=25, lp_mode=2):
        """Устанавливает начальные параметры работы с Long Poll VK API  

        Документация по Long Poll API: https://vk.com/dev/using_longpoll

        * group_id - идентификатор сообщества
        * access_token - ключ доступа к VK API 
        * lp_timewait - время ожидания (так как некоторые прокси-серверы обрывают 
                соединение после 30 секунд, мы рекомендуем указывать wait=25). 
                Максимальное значение — 90.
        * lp_mode = дополнительные опции ответа. Сумма кодов опций из списка:
            2 — получать вложения;
            8 — возвращать расширенный набор событий;
            32 — возвращать pts (это требуется для работы метода 
                messages.getLongPollHistory без ограничения в 256 последних 
                событий);
            64 — в событии с кодом 8 (друг стал онлайн) возвращать 
                дополнительные данные в поле $extra (см. Структура событий);
            128 — возвращать поле random_id (random_id может быть передан при 
                отправке сообщения методом messages.send).
        """
        super().__init__(name='longpoll_loop', daemon=False)


        self._access_token = os.getenv('VK_ACCESS_TOKEN', access_token)
        self._group_id = group_id        
        self._lp_timewait = lp_timewait
        self._lp_mode = lp_mode

        self._event_manager = Manager()
        self._listeners = self._event_manager.dict()

        self._default_listener = []

        self._workers = []

        self._request_key()

    def __del__(self):
        for p in self._workers:
            p.kill()
        self.kill()
    
    def _process_select(self, event):
        logging.debug("New event with type "+str(event['type']))
        for listener in self._listeners.get(event['type'], self._default_listener):
            listener(event)

    def _request_key(self):
        server_options = requests.get(f'{self.base_api_url}groups.getLongPollServer?v=5.52&group_id={self._group_id}&access_token={self._access_token}').json()
        logging.debug(server_options)
        self.lp_key = server_options['response']['key']
        self.lp_server = server_options['response']['server']
        self.lp_ts = server_options['response']['ts']
    
    def _make_lp_request(self):
        url = f'{self.lp_server}?act=a_check&key={self.lp_key}&ts={self.lp_ts}&wait={self._lp_timewait}&mode={self._lp_mode}&version=3'
        response = requests.get(url).json()

        error = response.get('failed', 0)
        if error == 1: 
            logging.warning("История событий устарела или была частично утеряна, приложение может получать события далее, используя новое значение ts из ответа.")
            self.lp_ts = response.get('ts',0)
            return []
        elif error == 2:
            logging.warning("Истекло время действия ключа, нужно заново получить key.")
            self._request_key()
            return []
        elif error == 3:
            logging.warning("Информация о пользователе утрачена, нужно запросить новые key")
            self._request_key()
            return []
        elif error == 4:
            logging.error("Передан недопустимый номер версии в параметре version")
            raise AttributeError("LongPoll API version is too old for work")
        else:
            self.lp_ts = response['ts']
            return response['updates']

    def run(self):
        while True:
            updates = self._make_lp_request()

            for u in updates:
                p = Process(target=self._process_select, args=(u,))
                p.authkey = os.urandom(16)
                self._workers.append(p)
                p.start()

            if os.getppid() == 1:
                logging.info("Parent process terminated, exiting...")
                for p in self._workers:
                    p.join()
                break

    def add_listener(self, event_type, listener_function):
        if event_type is None:
            self._default_listener.append(listener_function)
        elif event_type in self._listeners:
            self._listeners[event_type].append(listener_function)
        else: 
            self._listeners[event_type] = [listener_function]