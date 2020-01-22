from models.models import User
import requests


if __name__ == '__main__' :
    r = requests.get('https://github.com/timeline.json')
    print(r.text)
