import requests
import config
import json

def get_user_info(data = {}):
    url = '%s/api/users/getinfo/'%config.base_url
    res = requests.post(url, data=data)
    res.connection.close()
    if res.status_code == 200:
        return json.loads(res.text)['msg']
    else:
        return None
        
