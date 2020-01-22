from models.models import User
import requests
import settings

def make_request(user_id):
    url = settings.WEB_APP_URL
    data = {
            'user_id' : user_id
            }
    post = requests.post(url, data=data)
    return post

if __name__ == '__main__' :
    
    user_id = 1 #get from finger-print
    res = make_request(user_id)
    print(res.text)
    
