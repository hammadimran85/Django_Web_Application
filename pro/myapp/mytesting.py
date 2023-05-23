import requests

mysite=requests.get('http://127.0.0.1:8000/serializer/')
print(mysite.content)