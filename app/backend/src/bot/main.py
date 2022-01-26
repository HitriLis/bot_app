import copy
import glob
import os
from models import Message
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


    async def get_start_script(self, message, client_id):
        """
        Получение сообщения от бота при выполнении условий:
        :param message: Сообщение
        :param client_id: id клиент
        """
        
        if message.startswith("/start"):
           return  self.get_main_script()[0]

        last_script_bot = await Message.objects.get_last_script_bot(client_id)
        data = []
        for substring in self.NEGATIVE + self.POZITIVE:
            if substring in message.lower():
                status = 'negative' if substring in self.NEGATIVE else 'positive'
                script_next = self.get_script(last_script_bot)
                if last_script_bot == 'final' or script_next.get(status) is None:
                    status = 'final'
                is_script =  self.get_script(status) if status == 'final' else self.get_script(script_next.get(status))
                data = self.generate_answer(script=is_script, main=True)
                break
            else:
              data.append({'body': 'Попробуйте ещё раз', 'bot_script': None})
        
        return data[0]

 

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
