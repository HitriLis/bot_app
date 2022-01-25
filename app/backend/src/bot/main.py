import re
import copy
import glob
import os
from urllib.parse import urljoin

import yaml

from settings import settings



class Bot:
  
    POZITIVE = ('да', 'конечно', 'ага', 'пожалуй')
    NEGATIVE = ('нет', 'нет, конечно', 'ноуп', 'найн')

    def __init__(self, configs_root: str, static_url: str = None):
        self._configs_root: str = configs_root
        self._scripts: dict = {}

    async def declare(self):
        self._load_scripts()

    def _load_scripts(self) -> None:
        """
        Метод загружает все скрипты для бота из папки `bot/`
        """
        bot_configs = glob.glob(os.path.join(self._configs_root, "bot/") + "**/*.yaml", recursive=True)

        for config in bot_configs:
            scripts = yaml.load(open(config), Loader=yaml.FullLoader)

            for script in scripts:
                script_name = script.get('script')
                self._scripts[script_name] = script


    def get_script(self, script_name: str) -> dict:
        return self._scripts.get(script_name, {})
  


    def get_main_script(self) -> list:
        return self.generate_answer(script=self.get_script('main'), main=True)

    def get_main_script_answer(self):
        return {'status': self.STATUS_IGNORE_OPERATOR, 'data': self.get_main_script()}

    async def get_start_script(self, message, client_id):
        """
        Временно не актуально ибо переделывается, позже попарвим


        Получение стартового сообщения от бота при выполнении условий:
            1. Диалог с оператором не является активным
            2. Либо одно из условий:
                - Отсутствие какого-либо общения с ботом
                - Последний скрипт от бота относится к группе `feedback`

        :param last_script_bot: Последний скрипт бота
        """
        if message.startswith("/start"):
           return  self.get_main_script()

        data = {}
        for substring in self.NEGATIVE + self.POZITIVE:
            if substring in message.lower():
                status = 'negative' if substring in self.NEGATIVE else 'positive'
                data.update({'body': 'good', "ststus": status})
                break
            else:
              data.update({'body': 'Попробуйте ещё раз', 'bot_script': None})
        
        return data

 

    def get_script(self, script_name: str) -> dict:
        return self._scripts.get(script_name, {})


    async def get_answer(self, script_name: str = None, **kwargs) -> dict:
        """
        Получение ответа со сценарием от бота.
        Условия включения инлайн-скрипта:
            1. Название скрипта начинается на `//`
            2. Запрос на исполнение скрипта приходит с тестового сервера

        Условия вывода главного сообщения бота в момент отправки сообщения:
            - Последний скрипт бота относится к группе `feedback`
            - Последний диалог с оператором был закрыт &&
              Последнее сообщение от chat2desk с просьбой об оценке &&
              Сообщение от пользователя НЕ являются возможной оценкой: 1 или 2

        :param script_name: Название сценария
        :param kwargs:
            + client — Объект клиента
            + current_message — Текущее сообщение пользователя
        """
        client = kwargs.get('client')
        current_message = kwargs.get('current_message')

        if current_message.startswith("//"):
            data = await self._call_inline_func(**kwargs)
            return {"status": self.STATUS_IGNORE_OPERATOR, "data": data}

        is_open_c2d_dialog = await Client.objects.is_open_c2d_dialog(client.c2d_id)
        if is_open_c2d_dialog:
            return {'status': self.STATUS_TO_OPERATOR}
        if script_name:
            script_name = script_name.split('__')[-1]
        script_handler = getattr(self, f"_{script_name}", None)

        if script_name is not None and script_handler is not None and callable(script_handler):
            return await script_handler(**kwargs, script=self.get_script(script_name))

        if script_name is not None:
            return {
                'status': self.STATUS_IGNORE_OPERATOR,
                'data': self.generate_answer(script=self.get_script(script_name), **kwargs)
            }

        last_message = kwargs.get('last_message')
        if last_message.bot_script is not None and last_message.bot_script.startswith('feedback_'):
            return self.get_main_script_answer()

        if last_message.bot_script is not None and last_message.bot_script in self._scripts_before_to_operator:
            return await self._to_operator(**kwargs)

        if 'оператор' not in last_message.body and last_message.operator_id == self._operator.id:
            return await self._to_operator_first_message(**kwargs)

        return {'status': self.STATUS_TO_OPERATOR}


    def generate_answer(self, script: dict, **kwargs) -> list:
        """
        DEL
        Генерирование ответа для необходимого скрипта
        Если у скрипта есть указание на вызов дополнительного скрипта `finally`, то ответ будет дополнен этим скриптом
        :param script: Словарь с информацией о скрипте
        """
        result = []
        body = script.get('body', [])

        if isinstance(body, str):
            body = [body]

        for message in body:
            answer = copy.deepcopy(script)
            answer.update({'body': message, 'script_name': answer.pop('script', None)})
            result.append(answer)

        return result

   

    



    def get_include_scripts(self, script: dict, **kwargs) -> list:
        return [self._scripts[sc] for sc in script.get('include', []) if sc in self._scripts]



bot = Bot(
    configs_root=settings.configs_root,
    static_url=settings.static_url,
)
