import requests
import json
import random
def get_id(lis):
    temp=random.randint(1,1000)
    if temp in lis:
        return get_id(lis)
    else:
        return temp


try:
    file=open('store.txt','r')
    print(file.read())
    file.close
except:
    print("no file")
    data=requests.get('http://localhost:3000/handsake')
    lis=[x['device_id'] for x in json.loads(data.text)]
    device_id=get_id(lis)
    print(lis)
    address_line=input("Enter Address line:")
    pincode=int(input("Enter pincode::"))
    city=input("enter city:")
    district=input("Enter district:")
    state=input("enter state:")
    send_data={"address_line":address_line,"pincode":pincode,"district":district,"state":state,"device_id":device_id,"city":city}
    send_req=requests.post('http://localhost:3000/register',send_data)
    if send_req==200:
        print("successfully registered")
    else:
        print("error in registering")
    ssend=json.dumps(send_data)
    new_file=open('store.txt','w')
    new_file.writelines(ssend)
    new_file.close



