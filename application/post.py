import requests
import json

file=open("store.txt",'r')
obj=json.loads(file.read())
#print(obj['device_id'])
sendfire={"device_id":obj["device_id"],"status":"fire"}
send_req=requests.post('http://localhost:3000/firepost',sendfire)