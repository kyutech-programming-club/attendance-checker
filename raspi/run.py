from models.models import User
import requests
import settings
import datetime

def make_request(user_id):
    url = settings.WEB_APP_URL
    data = {
            'user_id' : user_id
            }
    post = requests.post(url, data=data)
    return post

if __name__ == '__main__' :
    
    user_id = 1 #get from finger-print
    res = make_request(user_id).json()
    expected_day = res['expected_day']
    sound_level = res['sound_level']
    user_id = res['user_id']
    print(datetime.datetime.fromtimestamp(expected_day))
    print(sound_level)
    print(user_id)
    
