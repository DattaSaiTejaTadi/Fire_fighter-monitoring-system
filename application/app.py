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




class Home(ttk.Frame):
   def __init__(self,container,customDesign,style):
      super().__init__(container,style=customDesign)
      self.style=style 
      self.createHomeFrame()
    
   def createHomeFrame(self):
      for child in self.winfo_children():
         child.destroy()
      self.label=ttk.Label(self,text="Details",style='sideheading.TLabel')
      self.label.place(x=20,y=150)
      self.v=tk.IntVar()
      self.startButton=ttk.Button(self,text="start",command=self.camCheck,style='custom.TButton')
      self.browseButton=ttk.Button(self,text = "Browse Files",command = self.browseFiles,style='custom.TButton')
      try:
         locationDetailsFile=open('locationDetails.txt','r')
         locationDetails=json.load(locationDetailsFile)
         locationDetailsFile.close()
         self.addresslabel=ttk.Label(self,text=f"Address: {locationDetails['address_line']}",style='custom.TLabel')
         self.addresslabel.place(x=30,y=200)
         self.locationlabel=ttk.Label(self,text=f"LocationId: {locationDetails['location_id']}",style='custom.TLabel')
         self.locationlabel.place(x=30,y=250)
         self.citylabel=ttk.Label(self,text=f"City: {locationDetails['city']}",style='custom.TLabel')
         self.citylabel.place(x=30,y=300)
         self.districtlabel=ttk.Label(self,text=f"District: {locationDetails['district']}",style='custom.TLabel')
         self.districtlabel.place(x=30,y=350)
         self.statelabel=ttk.Label(self,text=f"State: {locationDetails['state']}",style='custom.TLabel')
         self.statelabel.place(x=30,y=400)
         self.camButton=ttk.Radiobutton(self,text="Cam",variable=self.v,value=0 , command=self.showchoice,style='custom.TRadiobutton')
         self.camButton.place(x=150,y=20)
         self.testButton=ttk.Radiobutton(self,text="Test",variable=self.v,value=1,  command=self.showchoice,style='custom.TRadiobutton')
         self.testButton.place(x=300,y=20)
      except:
         self.label=ttk.Label(self,text="Location is not registered ,Register the location \n and restart app to use",foreground="red",font=("Helvetica", 15)).pack()

   def showchoice(self):
    if self.v.get()==0:
        self.startButton.place(x=190,y=75)
        self.browseButton.place_forget()
    else:
        self.browseButton.place(x=190,y=75)
        self.startButton.place_forget()
   def camCheck(self):
      self.detect_fire(0)
      
   def browseFiles(self):
      filename = filedialog.askopenfilename(initialdir = "/",  title = "Select a File",filetypes = (("video files",  "*.mp4*"),("all files", "*.*")))
      self.detect_fire(filename)

   def detect_fire(self,s):
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
                self.check(s)
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      cv2.destroyAllWindows()
      video.release()



     
   
   def check(self,s):
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
         file=open("locationDetails.txt",'r')
         obj=json.loads(file.read())
         file.close()
         send_req=requests.post('http://localhost:3000/firepost',obj)
         print("done")
      else:
         self.detect_fire(s)
      

class LocationRegister(ttk.Frame):
   def __init__(self,container,customDesign,style):
      super().__init__(container,style=customDesign)
      self.style=style
      self.configure(height=400,width=500)
      self.label=ttk.Label(self,text="Location Registeration",style='sideheading.TLabel').pack()
      self.address=tk.StringVar()
      self.pincode=tk.IntVar()
      self.city=tk.StringVar()
      self.district=tk.StringVar()
      self.state=tk.StringVar()
      try:
         self.locationsData=requests.get('http://localhost:3000/handsake')
         self.locationsList=[x['location_id'] for x in json.loads(self.locationsData.text)]
         self.location_id=self.get_id(self.locationsList)
         
      except requests.exceptions.RequestException as e:
         print(e)
         self.warningLabel=ttk.Label(self,text="problem in connecting to server",foreground="red",style='custom.TLabel').place(x=60,y=330)
      self.addressLabel=ttk.Label(self,text="Address:",style='custom.TLabel').place(x=60,y=60)
      self.addressEntry=ttk.Entry(self,textvariable=self.address)
      self.addressEntry.place(x=200,y=60)
      self.pincodeLabel=ttk.Label(self,text="Pincode:",style='custom.TLabel').place(x=60,y=100)
      self.pincodeEntry=ttk.Entry(self,textvariable=self.pincode)
      self.pincodeEntry.place(x=200,y=100)
      self.cityLabel=ttk.Label(self,text="City:",style='custom.TLabel').place(x=60,y=140)
      self.cityEntry=ttk.Entry(self,textvariable=self.city)
      self.cityEntry.place(x=200,y=140)
      self.districtLabel=ttk.Label(self,text="District:",style='custom.TLabel').place(x=60,y=180)
      self.districtEntry=ttk.Entry(self,textvariable=self.district)
      self.districtEntry.place(x=200,y=180)
      self.stateLabel=ttk.Label(self,text="State:",style='custom.TLabel').place(x=60,y=220)
      self.stateEntry=ttk.Entry(self,textvariable=self.state)
      self.stateEntry.place(x=200,y=220)
      self.registerButton=ttk.Button(self,style='custom.TButton',text="Register",command=self.registerLocation).place(x=30,y=280)
      self.clearButton=ttk.Button(self,style='custom.TButton',text="Clear",command=self.clear).place(x=300,y=280)

   def clear(self):
      os.remove('locationDetails.txt')
      self.master.home_frame.createHomeFrame()

   def registerLocation(self):
      send_data={"address_line":self.address.get(),"pincode":self.pincode.get(),"district":self.district.get(),"state":self.state.get(),"location_id":self.location_id,"city":self.city.get()}   
      try:
         send_req=requests.post('http://localhost:3000/register',send_data) 
         ssend=json.dumps(send_data)
         new_file=open('locationDetails.txt','w')
         new_file.writelines(ssend)
         new_file.close()
         self.master.home_frame.createHomeFrame()
         self.master.CiviliansRegistration_frame.createPage()

      except requests.exceptions.RequestException as e:
         self.warningLabel=ttk.Label(self,text="problem in registering",foreground="red",font=("Helvetica", 15)).pack()
      self.addressEntry.delete(0,tk.END)
      self.pincodeEntry.delete(0,tk.END)
      self.cityEntry.delete(0,tk.END)
      self.districtEntry.delete(0,tk.END)
      self.stateEntry.delete(0,tk.END)
      
   def get_id(self,lis):
      temp=random.randint(1,1000)
      if temp in lis:
         return LocationRegister.get_id(lis)
      else:
         return temp
      
class CiviliansRegisteration(ttk.Frame):
   def __init__(self,container,customDesign,style):
      super().__init__(container,style=customDesign)
      self.style=style
      self.createPage()
      
   def createPage(self):
      for child in self.winfo_children():
         child.destroy()
      self.name=tk.StringVar()
      self.phone=tk.StringVar()
      try:
         file=open('locationDetails.txt','r')
         self.obj=json.loads(file.readline())
         file.close()
         self.location_id=self.obj['location_id']
      except:
         print("err")
      self.registerLabel=ttk.Label(self,text="Regiater Civilians",style='sideheading.TLabel').place(x=20,y=20)
      self.nameLabel=ttk.Label(self,text="Name : ",style='custom.TLabel').place(x=50,y=60)
      self.nameEntry=ttk.Entry(self,textvariable=self.name)
      self.nameEntry.place(x=150,y=60)
      self.phoneLabel=ttk.Label(self,text="Phone : ",style='custom.TLabel').place(x=50,y=100)
      self.phoneEntry=ttk.Entry(self,textvariable=self.phone)
      self.phoneEntry.place(x=150,y=100)
      self.registerButton=ttk.Button(self,text="Add user",style='custom.TButton',command=self.addUser).place(x=100,y=140)
      try:
         self.res=requests.post('http://localhost:3000/getusers',self.obj)
         self.user_list=json.loads(self.res.text)
         self.civiliantable = ttk.Treeview(self, columns=("name", "phone"))
         self.civiliantable.heading("#0", text="id")
         self.civiliantable.heading("name", text="name")
         self.civiliantable.heading("phone", text="phone")
         self.civiliantable.column("#0", width=50, anchor="center")
         self.civiliantable.column("name", width=100, anchor="center")
         self.civiliantable.column("phone", width=140, anchor="center")
         self.i=0
         for user in self.user_list:
            self.i+=1
            self.civiliantable.insert("", "end", text=str(self.i), values=(user['name'],user['phone'] ))
         self.userdata_label=ttk.Label(self,text="Users data",style='sideheading.TLabel')
         self.userdata_label.place(x=20,y=180)
         self.civiliantable.place(x=50,y=230)
         
      except:
         self.warningLabel=ttk.Label(self,text="Could not connect to the server check the connection",foreground="red",font=("Helvetica", 15)).place(x=20,y=170)

   def addUser(self):
    lis=[]
    lis.append({'name':self.name.get(),'phone':self.phone.get(),'location_id':self.location_id})
    send_req=requests.post('http://localhost:3000/registerpeople',json=lis)
    self.nameEntry.delete(0,tk.END)
    self.phoneEntry.delete(0,tk.END)
    self.createPage()


class Notebook(ttk.Notebook):
   def __init__(self,container,customeStyle,design):
      super().__init__(container,style=customeStyle)
      self.style=design
      self.home_frame=Home(self,'custom.TFrame',self.style)
      self.location_frame=LocationRegister(self,'custom.TFrame',self.style)
      self.CiviliansRegistration_frame=CiviliansRegisteration(self,'custom.TFrame',self.style)
      self.home_frame.pack()
      self.location_frame.pack()
      self.CiviliansRegistration_frame.pack()
      self.add(self.home_frame,text='Home')
      self.add(self.location_frame,text='Register location')
      self.add(self.CiviliansRegistration_frame,text='Civilians Data')


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.style=ttk.Style()
        self.style.configure('custom.TFrame',foreground="black",background="whitesmoke")
        self.style.configure('custom.TLabel',foreground="black",background="whitesmoke",font=" helvetica 15")
        self.style.configure('sideheading.TLabel',foreground="#0080FE",background="whitesmoke",font=" helvetica 20")
        self.style.configure('custom.TRadiobutton',foreground="black",background="whitesmoke",font=" helvetica 20")
        self.style.configure('custom.TButton',bg='#0080FE',fg='#000000',font=" helvetica 15")
        self.style.configure('custom.TNotebook', tabmargins=[2, 5, 2, 0],background='white')
        self.style.configure('custom.TNotebook.Tab',padding=[20, 5], font=('TkDefaultFont', 11, 'bold'), background='white', foreground='#0080FE')
        self.style.map('Custom.TNotebook.Tab', background=[('selected', '#E74C3C'), ('active', '#FF5733')], foreground=[('selected', '#0080FE'), ('active', '#0080FE')])
        self.style.configure('main.TLabel',foreground="#0018F9",background="white",font="georgia  20")
        self.title("FSM")
        self.config(background='white')
        self.geometry('600x600+100+100')
        self.iconbitmap('images.ico')
        self.label = ttk.Label(self, text='Automatic Fire alarm system using\n              surveilance cameras',style='main.TLabel')
        self.label.pack()
        self.notebook=Notebook(self,'custom.TNotebook',self.style)
        self.notebook.pack(expand=True ,fill="both",padx=20)


if __name__ == "__main__":
  try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
  finally:
    
    app = App()
    app.mainloop()
