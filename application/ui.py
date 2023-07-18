import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import numpy as np
import time
import requests
import json
import random
import os
import time


def get_id(lis):
    temp=random.randint(1,1000)
    if temp in lis:
        return get_id(lis)
    else:
        return temp
def check():
    img1 = cv2.imread('image1.png')
    img2 = cv2.imread('image2.png')
    os.remove('image1.png')
    os.remove('image2.png')


# convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# define the function to compute MSE between two images
    def mse(img1, img2):
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse, diff

    error, diff = mse(img1, img2)
    print("Image matching Error between the two images:",error)
    if error>=1:
        file=open("store.txt",'r')
        obj=json.loads(file.read())
        file.close()
        send_req=requests.post('http://localhost:3000/firepost',obj)
        print("done")
    else:
        detect_fire()
def detect_fire(s):
    print(s)
    video = cv2.VideoCapture(s)
    fp=0
    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
          break
 
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
        lower = [18, 50, 50]
        upper = [35, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
    
 
 
        output = cv2.bitwise_and(frame, hsv, mask=mask)
        no_red = cv2.countNonZero(mask)
        cv2.imshow("output", output)
    #print("output:", frame)
        if int(no_red) > 20000:
            print ('Fire detected')
            fp=fp+1
            if fp==1:
                frame1=output
                cv2.imwrite('image1.png', output)
            time.sleep(1)
            if fp==2:
                frame2=output
                cv2.imwrite('image2.png', output)
                check()
                break

        #req=requests.get("http://localhost:3000/alarm")
    #print(int(no_red))
   #print("output:".format(mask))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    video.release()

window=tk.Tk()
window.geometry("1100x770+0+0")
window.title("Video capture")
window.config(bg="black")
window.config(highlightbackground="blue",highlightthickness=3)

#frame1 logic
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",  title = "Select a File",filetypes = (("video files",  "*.mp4*"),("all files", "*.*")))
    detect_fire(filename)
def camCheck():
    detect_fire(0)

frame1=tk.Frame(window,height=700,width=500,bg="#121212",highlightthickness=0)
frame1.grid_propagate(False)
frame1.grid(row=0,column=0,padx=15,pady=5)
v=tk.IntVar()
cstart=tk.Button(frame1,text="start",command=camCheck,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30},)
browsefiles=tk.Button(frame1,text = "Browse Files",command = browseFiles,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30},)
#tstart= tk.Button(frame1,text="start",command=testCheck)
def showchoice():
    #print(v.get())
    if v.get()==0:
        cstart.place(x=190,y=70)
        browsefiles.place_forget()
        #tstart.grid_forget()
    else:
        browsefiles.place(x=180,y=70)
        #tstart.grid(row=3,column=0,pady=15)
        cstart.place_forget()
tk.Radiobutton(frame1,text="Cam",variable=v,value=0 ,font={"Helvetica bold",30} , command=showchoice,fg="whitesmoke",bg="#121212").place(x=100,y=20)
tk.Radiobutton(frame1,text="Test",variable=v,value=1,font={"Helvetica bold",30},  command=showchoice,fg="whitesmoke",bg="#121212").place(x=260,y=20)

style = ttk.Style(frame1)
# set ttk theme to "clam" which support the fieldbackground option
style.theme_use("clam")
style.configure("Treeview", background="#121212", foreground="whitesmoke")
style.configure("Treeview.Heading",foreground="whitesmoke", background="#121212")
tree = ttk.Treeview(frame1, columns=("address", "location_id", "district","pincode","city","state"))
tree.heading("#0", text="Item")
tree.heading("address", text="address")
tree.heading("location_id", text="location_id")
tree.heading("district", text="district")
tree.heading("pincode", text="pincode")
tree.heading("city", text="city")
tree.heading("state", text="state")
tree.column("#0", width=40, anchor="center")
tree.column("address", width=80, anchor="center")
tree.column("location_id", width=60, anchor="center")
tree.column("district", width=90, anchor="center")
tree.column("pincode", width=60, anchor="center")
tree.column("city", width=60, anchor="center")
tree.column("state",width=90,anchor="center")
data_label=tk.Label(frame1,text="Device data",fg="whitesmoke",bg="#121212" ,font={"Helvetica bold",50,"bold"})
data_label.place(x=180,y=130)
tree.place(x=10,y=180)
file=open('store.txt','r')
obj=json.loads(file.readline())
file.close()
tree.insert("", "end", text="Row 1",tags=("rows"), values=(obj['address_line'],obj['location_id'],obj['district'],obj['pincode'],obj['city'],obj['state']))
tree.tag_configure("rows",foreground="whitesmoke", background="#121212")
res=requests.post('http://localhost:3000/getusers',obj)
#print(type(res.text))
user_list=json.loads(res.text)
tree2 = ttk.Treeview(frame1, columns=("name", "phone"))
tree2.heading("#0", text="id")
tree2.heading("name", text="name")
tree2.heading("phone", text="phone")
tree2.column("#0", width=100, anchor="center")
tree2.column("name", width=100, anchor="center")
tree2.column("phone", width=100, anchor="center")
i=0
for user in user_list:
    i+=1
    tree2.insert("", "end", text=str(i), values=(user['name'],user['phone'] ))
userdata_label=tk.Label(frame1,text="Users data",fg="whitesmoke",bg="#121212" ,font={"Helvetica bold",30})
userdata_label.place(x=180,y=430)
tree2.place(x=70,y=465)


framez=tk.Frame(window,height=750,width=470,bg="black")
framez.grid_propagate(False)
framez.grid(row=0,column=1,padx=15,pady=5)

#frame 2 logic
address=tk.StringVar()
pincode=tk.IntVar()
city=tk.StringVar()
district=tk.StringVar()
state=tk.StringVar()
def register():
    data=requests.get('http://localhost:3000/handsake')
    lis=[x['location_id'] for x in json.loads(data.text)]
    location_id=get_id(lis)
    send_data={"address_line":address.get(),"pincode":pincode.get(),"district":district.get(),"state":state.get(),"location_id":location_id,"city":city.get()}
    send_req=requests.post('http://localhost:3000/register',send_data)
    ssend=json.dumps(send_data)
    new_file=open('store.txt','w')
    new_file.writelines(ssend)
    new_file.close()
    time.sleep(2)
    window.update()
def clearData():
    os.remove('store.txt')
    time.sleep(1)
    window.update()
frame2=tk.Frame(framez,height=430,width=465,bg="#121212",highlightthickness=0)
frame2.grid_propagate(False)
frame2.grid(row=0,column=0,pady=30)
label1=tk.Label(frame2,text="Device Registration",fg="whitesmoke",bg="#121212" ,font={"Helvetica bold",30})

label1.grid(row=0,column=0,columnspan=2 ,pady=20,padx=140)
label_address=tk.Label(frame2,text="Address",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
address_entry=tk.Entry(frame2,textvariable=address)
label_address.grid(row=1,column=0,pady=15)
address_entry.grid(row=1,column=1,pady=15)
label_pincode=tk.Label(frame2,text="Pincode",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
pincode_entry=tk.Entry(frame2,textvariable=pincode)
label_pincode.grid(row=2,column=0,pady=15)
pincode_entry.grid(row=2,column=1,pady=15)
label_city=tk.Label(frame2,text="City",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
city_entry=tk.Entry(frame2,textvariable=city)
label_city.grid(row=3,column=0,pady=15)
city_entry.grid(row=3,column=1,pady=15)
label_district=tk.Label(frame2,text="District",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
district_entry=tk.Entry(frame2,textvariable=district)
label_district.grid(row=4,column=0,pady=15)
district_entry.grid(row=4,column=1,pady=15)

label_state=tk.Label(frame2,text="State",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
state_entry=tk.Entry(frame2,textvariable=state)
label_state.grid(row=5,column=0,pady=15)
state_entry.grid(row=5,column=1,pady=15)

registerd=tk.Button(frame2,text="Register",command=register,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
clear=tk.Button(frame2,text="clear",command=clearData,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
registerd.grid(row=6,column=0,pady=15)
clear.grid(row=6,column=1,pady=15)




#frame3 logic
frame3=tk.Frame(framez,height=245,width=465,bg="#121212",highlightthickness=0)
frame3.grid_propagate(False)
frame3.grid(row=1,column=0,pady=5)
label2=tk.Label(frame3,text="User Registration" ,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
label2.grid(row=0,column=0,columnspan=2 ,pady=20,padx=140)

name=tk.StringVar()
phone=tk.StringVar()
def addUser():
    file=open('locationDetails.txt','r')
    obj=json.loads(file.readline())
    location_id=obj['device_id']
    lis=[]
    lis.append({'name':name.get(),'phone':phone.get(),'location_id':location_id})
    send_req=requests.post('http://localhost:3000/registerpeople',json=lis)
    file.close()
    

label_name=tk.Label(frame3,text="Name",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
name_entry=tk.Entry(frame3,textvariable=name)
label_name.grid(row=1,column=0,pady=15)
name_entry.grid(row=1,column=1,pady=15)

label_phone=tk.Label(frame3,text="Phone no",fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
phone_entry=tk.Entry(frame3,textvariable=phone)
label_phone.grid(row=2,column=0,pady=15)
phone_entry.grid(row=2,column=1,pady=15)

log=tk.Button(frame3,text="Add user",command=addUser,fg="whitesmoke",bg="#121212",font={"Helvetica bold",30})
log.grid(row=3,column=0,columnspan=2, pady=15)



window.resizable(width=False,height=False)
window.mainloop()