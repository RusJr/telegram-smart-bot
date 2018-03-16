import execjs
import requests

from p_bot.sign import PBotSign
from utils.requester import Requester


class MessageHistory:
    def __init__(self, depth=3):
        self.depth = depth
        self._storage = []

    def append(self, request: str, answer: str) -> None:
        self._storage.append((request, answer))
        if len(self._storage) > self.depth:
            self._storage.pop(0)

    def get_dict(self):
        result = {}
        for idx, (request, answer) in enumerate(self._storage[::-1], 1):
            result['request_%d' % idx] = request
            result['answer_%d' % idx] = answer
        return result


class PBot:

    _get_answer_url = 'http://p-bot.ru/api/getAnswer'
    _headers = {'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'p-bot.ru',
                'Origin': 'http://p-bot.ru',
                'Referer': 'http://p-bot.ru/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    _bot_name = 'ρBot'
    _dialog_lang = 'ru'
    _dialog_greeting = False

    def __init__(self, user_name='Незнакомец'):
        self.user_name = user_name
        self._history = MessageHistory()
        self._dialog_id = self._create_dialog_id()
        self._session = requests.Session()
        self._session.cookies.update({'dialog_id': self._dialog_id})

    def get_answer(self, client_message: str):

        request_params = {'method': 'POST',
                          'url': self._get_answer_url,
                          'headers': self._headers,
                          'data': self._get_request_data(client_message)}
        status, response_data = Requester.request_and_parse(request_params, session=self._session)

        try:
            answer = response_data['answer']
        except KeyError:
            answer = 'pbErr (%d)' % status
        else:
            self._history.append(client_message, answer)
        return answer

    def _get_request_data(self, client_message: str) -> dict:
        data = {'request': client_message,
                'bot_name': self._bot_name,
                'user_name': self.user_name,
                'dialog_lang': self._dialog_lang,
                'dialog_id': self._dialog_id,
                'dialog_greeting': self._dialog_greeting, }
        data.update(PBotSign().to_dict())
        data.update(self._history.get_dict())
        return data

    @staticmethod
    def _create_dialog_id() -> str:
        js = execjs.compile("""
            _uuidv4 = function() {
              return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"["replace"](
                /[xy]/g,
                function(_0x24cc45) {
                  var _0x1e28f8 = (Math["random"]() * 0x10) | 0x0,
                    _0xea8175 = _0x24cc45 == "x" ? _0x1e28f8 : (_0x1e28f8 & 0x3) | 0x8;
                  return _0xea8175["toString"](0x10);
                }
              );
            };
        """)
        return js.call("_uuidv4")


if __name__ == '__main__':
    p_bot = PBot('Rus')
    print(p_bot.get_answer('Кто я?'))
