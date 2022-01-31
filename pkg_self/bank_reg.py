from tkinter import *
import mysql.connector as mys
from aes_crypt import encrypt as enc
from aes_crypt import decrypt as dec

def sub():
    global b2,c2,d2,e2
    b2 = b1.get()
    c2 = c1.get()
    d2 = d1.get()
    e2 = e1.get()
    if not b2.isalpha():
        win2 = Toplevel(win)
        Label(win2,text = "Invalid name").pack()
        return
    if len(c2) < 8:
          win2 = Toplevel(win)
          Label(win2,text = "Password should be atleast 8 characters").pack()
          return
    if not d2.isdigit() or len(d2) != 4 or d2 == "0000":
          win2 = Toplevel(win)
          Label(win2,text = "bad pin").pack()
          return
    try:
         x = float(e2)
    except:
         win2 = Toplevel(win)
         Label(win2,text = "invalid balance").pack()
         return
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("Select * from account")
    regid = "DBOI"+str(cur.rowcount+1)
    win2 = Toplevel(win)
    Label(win2,text = "regid: "+regid).pack()
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("insert into account values(%s,%s,%s,%s,%s)",(regid,b2,enc(c2,d2),enc(d2,c2),enc(enc(e2,d2),c2)))
    obj.commit()

  
win = Tk()
a = Label(win,text="Registration Details").pack()

b = Label(win,text="Name").pack()
c = Label(win,text="Password").pack()
d = Label(win,text="Pin").pack()
e = Label(win,text="Deposit").pack()
b1 = Entry(win,width = 50)
b1.pack()
c1 = Entry(win,width = 30)
c1.pack()
d1 = Entry(win,width = 4)
d1.pack()
e1 = Entry(win,width = 10)
e1.pack()
f = Button(win,text="Submit",command = sub).pack()
win.mainloop()

