import requests

re = requests.get("http://140.113.178.132:3017/group/1/bulletins/")
print(re.text)
