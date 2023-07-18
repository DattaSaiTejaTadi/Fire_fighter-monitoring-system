import requests
import json
n=int(input("Enter number of people:"))
lis=[]
file=open('store.txt','r+')
obj=json.loads(file.readline())
device_id=obj['device_id']
for i in range(n):
    name=input("Enter name of person:")
    phone=input("enter mobile number of person:")
    lis.append({'name':name,'phone':phone,'device_id':device_id})
print(lis)
send_req=requests.post('http://localhost:3000/registerpeople',json=lis)
print("successfulluy registered")

file.writelines(json.dumps(lis))
file.close