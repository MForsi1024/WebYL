from flask import Flask, request, jsonify
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


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

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз

        sessionStorage[user_id] = {
            'suggests': [{'title': 'да', 'hide': True}, {'title': 'нет', 'hide': True}, {'title': 'справка', 'hide': True}],
            "waiting_for_word": False
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Я умею переводить сленговые слова. Что-то интересует?'
        res['response']['buttons'] = sessionStorage[user_id]["suggests"]
        return
    if sessionStorage[user_id]["waiting_for_word"]:
        znacheniye(req['request']['original_utterance'])
        res['response']['text'] = f'{req['request']['original_utterance']}'
        return

    elif "да" in req['request']['original_utterance']:
        sessionStorage[user_id]["waiting_for_word"] = True
        res['response']['text'] = 'Хорошо, приступим! Какое слово тебе объяснить? Напиши просто это слово.'
        return

    elif "нет" in req['request']['original_utterance']:
        res['response']['text'] = 'Ну, как знаешь. Пока!'
        res['response']['end_session'] = True
        return

    else:
        res['response']['text'] = 'Не поняла. Повтори пожалуйста.'
        return


def znacheniye(word):
    print(word)


if __name__ == '__main__':
    app.run()
