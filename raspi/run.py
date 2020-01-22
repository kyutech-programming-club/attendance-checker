from models.models import User
import requests
import settings

if __name__ == '__main__' :
    url = settings.WEB_APP_URL
    data = {
            'message' : 'Hello, World'
            }
    res = requests.post(url, data=data)
    print(res.text)
    
