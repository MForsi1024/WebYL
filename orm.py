import json

import requests
def get_response(req, url):
  response = requests.get(url + "/get?word=" + req).content
  response = response.decode('utf-8')
  parsed = json.loads(response)
  return parsed["word"]

print(get_response("черемша", 'http://127.0.0.1:6767'))
