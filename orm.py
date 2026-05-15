import json

import requests
def get_response(req, url):
  response = requests.get(url + "/get?word=" + req.lower()).content
  response = response.decode('utf-8')
  parsed = json.loads(response)
  return parsed["word"]
