import requests
import json

data=requests.get('http://localhost:3000/getlocations');
print(type(data.text))
print(data.text)
file=open('locations.txt','w')
file.write(data.text)