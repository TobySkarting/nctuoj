import requests
import config
import json

def get_token(data = {}):
    url = '%s/api/users/gettoken/'%config.base_url
    res = requests.post(url, data=data)
    res.connection.close()
    if res.status_code == 200:
        return json.loads(res.text)['msg']
    else:
        return None
        
