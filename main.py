from flask import Flask, request, jsonify
import logging
import orm
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

URL = 'http://127.0.0.1:6767'
@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    req_text = req['request']['original_utterance'].lower()
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз

        sessionStorage[user_id] = {
            'suggests': [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True},
                         {'title': 'Справка', 'hide': True}],
            "waiting_for_word": False
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Привет!'
        res['response']['buttons'] = sessionStorage[user_id]["suggests"]
        res['response']['card'] = {
            'type': 'BigImage',
            'image_id': '1030494/d5c0fc62190df2ce0c9d',
            'title': 'Привет!',
            'description': 'Я умею переводить сленговые слова на понятный язык. Хочешь что-то перевести?'
        }
        return
    if sessionStorage[user_id]["waiting_for_word"]:
        meaning = get_meaning(req['request']['original_utterance'])
        res['response']['text'] = f'{meaning}. Следующее слово?'
        return

    elif "да" in req_text:
        sessionStorage[user_id]["waiting_for_word"] = True
        res['response']['text'] = 'Хорошо, приступим! Какое слово тебе объяснить? Напиши интересующее тебя слово.'
        return

    elif "нет" in req_text:
        res['response']['text'] = 'Ну, как знаешь. Пока!'
        res['response']['end_session'] = True
        return

    elif "справка" in req_text or "помощь" in req_text:
        res['response']['text'] = ('Я могу объяснить тебе значение современных сленговых слов.'
                                   ' После того, как ты ответишь "Да" на мой вопрос, ты по одному отправляешь мне слова,'
                                   ' значения которых тебя интересуют. К каждому слову я тебе буду делать описание.'
                                   ' Начнём?')
        res['response']['buttons'] = sessionStorage[user_id]["suggests"]
        res['response']['card'] = {
            'type': 'BigImage',
            'image_id': '13200873/b046eadeb9653b25600a',
            'title': 'Помощь!',
            'description': 'Я могу объяснить тебе значение современных сленговых слов.'
                                   ' После того, как ты ответишь "Да" на мой вопрос, ты по одному отправляешь мне слова,'
                                   ' значения которых тебя интересуют. К каждому слову я тебе буду делать описание.'
                                   ' Начнём?'
        }
        return

    else:
        res['response']['text'] = 'К сожалению я не понимаю тебя, пожалуйста скажи "Да", "Нет" или "Справка".'
        res['response']['buttons'] = sessionStorage[user_id]["suggests"]
        return


def get_meaning(word):
    return orm.get_response(word, URL)


if __name__ == '__main__':
    app.run()
