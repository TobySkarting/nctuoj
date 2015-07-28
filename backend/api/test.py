import requests


def api_user_signup():
    data = {'account': 'test',
            'student_id': 'XD',
            'passwd': 'gg',
            'repasswd': 'gg'
            }
    url = 'http://localhost:3017/api/user/signup/'
    r = requests.post(url, data=data)
    print(r.text)

def api_user_list():
    url = "http://localhost:3017/api/user/"
    r = requests.get(url)
    print(r.text)
api_user_signup()
api_user_list()
