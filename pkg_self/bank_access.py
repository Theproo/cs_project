from tkinter import *
import mysql.connector as mys
from aes_crypt import  encrypt as enc
from aes_crypt import  decrypt as dec
from functools import partial

def de2(x):
    e2 = x.get()
    try:
        y =float(e2)
        if y<0:
            win4 = Toplevel()
            Label(win4,text = "Invalid amount deposited").pack()
            return
    except:
        win4 = Toplevel()
        Label(win4,text = "Invalid amount deposited").pack()
        return
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("select * from account where regid = "+f"'{b2}'")
    tup = cur.fetchone()
    bal = (dec(dec(tup[4],c2),d2)).strip()
    bal = float(bal) + y
    newbal = enc(enc(str(bal),d2),c2)
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("update account set balance =" + f"'{newbal}'" + "where regid = " + f"'{b2}'")
    obj.commit()
    win4 = Toplevel()
    Label(win4,text = "Successfully deposited").pack()
    return

def deposit():
    win3 = Toplevel()
    Label(win3,text = "Amount to be deposited: ").pack()
    e1 = Entry(win3,width = 10)
    e1.pack()
    f = Button(win3,text="Deposit",command = partial(de2,e1)).pack()
def wi2(t):
    e2 = t[1].get()
    try:     
      if float(e2) > float(t[0]):
           win4 = Toplevel()
           Label(win4,text = "Insufficient Money").pack()
           Label(win4,text = "Your Balance: "+t[0]).pack()
           return
    except:
        win4 = Toplevel()
        Label(win4,text = "Invalid amount withdrawn").pack()
        return
    if float(e2) <0:
        win4 = Toplevel()
        Label(win4,text = "Invalid amount withdrawn").pack()
        return
    bal = str(float(t[0])-float(e2))
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    newbal = enc(enc(bal,d2),c2)
    cur.execute("update account set balance = " + f"'{newbal}'" + "where regid = " + f"'{b2}'")
    obj.commit()
    win4 = Toplevel()
    Label(win4,text = "Successfully withdrawn").pack()
    return
    
def withdraw():
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("select * from account where regid = "+f"'{b2}'")
    tup = cur.fetchone()
    balance = dec(dec(tup[4],c2),d2)
    win3 = Toplevel()
    Label(win3,text = "Amount to be withdrawn: ").pack()
    e1 = Entry(win3,width = 10)
    e1.pack()
    t = (balance.strip(),e1)
    f = Button(win3,text="Withdraw",command = partial(wi2,t)).pack()
    
        
def check_balance():
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("select * from account where regid = "+f"'{b2}'")
    tup = cur.fetchone()
    balance = dec(dec(tup[4],c2),d2)
    win3 = Toplevel()
    Label(win3,text = "Your Balance: "+balance).pack()
      
def access():
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("select * from account where regid = "+f"'{b2}'")
    tup = cur.fetchone()
    win2 = Toplevel(win)
    Label(win2,text = "Welcome  "+tup[1]).pack()
    Button(win2,text="withdraw",command = withdraw).pack()
    Button(win2,text="deposit",command = deposit).pack()
    Button(win2,text="check balance",command = check_balance).pack()
    
def sub():
    global b2,c2,d2
    b2 = b1.get()
    c2 = c1.get()
    d2 = d1.get()
    obj = mys.connect(host = "localhost",username = "root",password ="QWERTY1234uiop!@#$",port = 3300,database="dboi")
    cur = obj.cursor()
    cur.execute("select * from account where regid = "+f"'{b2}'")
    tup = cur.fetchall()
    if len(tup) == 0:
        win2 = Toplevel()
        Label(win2,text = "Invalid ID").pack()
        return
    if enc(c2,d2) != tup[0][2] or enc(d2,c2) != tup[0][3]:
        win2 = Toplevel(win)
        Label(win2,text = "Authentication Failed").pack()
        return
    access()
   
   
#Login
win = Tk()
win.title("Digital Bank Of India")
a = Label(win,text="Login").pack()
b = Label(win,text="Registration ID").pack()
b1 = Entry(win,width = 50)
b1.pack()
c = Label(win,text="Password").pack()
d = Label(win,text="Pin").pack()
c1 = Entry(win,width = 30)
c1.pack()
d1 = Entry(win,width = 4)
d1.pack()
e = Button(win,text="Submit",command = sub).pack()
win.mainloop()
