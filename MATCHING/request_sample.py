from __future__ import print_function
import requests
import json
import random

def change_word(word):
    url = "http://35.190.216.222:8000"
    payload = {"words":[word]}
    response = requests.post(url, data = json.dumps(payload))
    text = json.loads(response.text)
    return text['matched'][0]

def get_wrong_words(l):
    result = []
    for obj in l:
        words = obj.split()
        n = len(words)
        extract = random.randint(0, n - 1)
        words[extract] = change_word(words[extract])
        obj = ' '.join(words)
        result.append(obj)
    return result

l = ['șira spinării', 'măsea', 'dinti', 'vomă', 'miop', 'MEDICATIE', 'bisturiu']
print(get_wrong_words(l))
