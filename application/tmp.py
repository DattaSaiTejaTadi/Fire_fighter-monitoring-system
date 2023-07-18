import requests
import json

data=requests.get('http://localhost:3000/tempdata');
print(type(data.text))
print(data.text)
file=open('tmp.txt','w')
file.write(data.text)