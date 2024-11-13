import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import tkinter.scrolledtext as tkst
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
import serial.tools.list_ports
import List_COM_ports
import sys
from sys import exit
import locus
from pprint import pformat
from datetime import datetime
import os
import serial
# from pathlib import Path
from time import sleep
import time
from threading import *

def centre_window(w, h):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = 50 #(ws/2)
    y = 50#(hs/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def get_ok(port,s_msg = 0):
    global t_y, s_id

    if(s_msg =="2"):
        now = datetime.now()
        snow = now.strftime("%Y%m%d")
        print(l_fname.get() + "_" + str(snow) + ".log")
        file_name = l_fname.get() +"_"+str(snow)+ ".log"
        # Dump_file = open("Download_Cache1.log","w")
        Dump_file = open(file_name,"w")
    y = "NA"
    b_id = 0
    tstart = time.time()
    while(y.rstrip() != "OK" and time.time() - tstart < 1):
        y=port.readline().decode('utf-8')[:-1]
        if(s_msg == "1" or s_msg == "5"or s_msg == "8" or s_msg == "9"):
            print(str(y))
        print(str(y))
        if(y.rstrip() != "OK"):
            if(s_msg == "2"): #download data
                Dump_file.write(str(y))
                if y=="\n":
                     Dump_file.seek(0)
                     Dump_file.truncate()
                Dump_file.flush()
            if(s_msg == "1" and b_id == 0): #initial comms
                s_id = y
                b_id = 1
            t_y = y
        if(len(y) > 1):
            tstart = time.time()

    if(y.rstrip() == "OK"):
        b_ok = 1
    else:
        b_ok = 0
    if(s_msg == "2"):
        Dump_file.close()
    return(b_ok)

def send_msg(Com_Port,s_msg,t_init = 0):
    b_ok = 0
    port = serial.Serial(Com_Port, baudrate=9600, timeout= 3.0)
    # s_msg = "$4" #
    s_msg2 = "$"+str(s_msg)
    port.write(s_msg2.encode('utf-8'))
    if(get_ok(port)):
        if(t_init !=0):
            port.write(t_init.encode('utf-8'))
        if(get_ok(port,s_msg)):
            b_ok = 1

    port.close()
    return(b_ok)


def on_select(event=None):
    btn_Connect["state"] = "normal"

def connect():
    global t1,t2,t3,t4,t5,t6,t7,t8,t_y,Com_Port,s_id
    # answer = tk.messagebox.askokcancel("Connect", "Switch on device on press OK")
    # if(answer):
    btn_Refresh["state"] = "disabled"
    btn_Connect["state"] = "disabled"
    Com_Port = cb.get()

    if(send_msg(Com_Port,"1")):
        print("Port selected: ", Com_Port)
        print(t_y)
        print(s_id)
        print(s_id[0:2])
        if(s_id[0:2] == "AC"):
            print("Model AC")
            vals = t_y.split(',')
            try:
                t1 = vals[0]
            except:
                t1 = 0
            try:
                t2 = vals[1]
            except:
                t2 = 0
            try:
                t3 = vals[2]
            except:
                t3 = 0
            try:
                t4 = vals[3]
            except:
                t4 = 0
            try:
                t5 = vals[4]
            except:
                t5 = 0
            try:
                t6 = vals[5]
            except:
                t6 = 0
            try:
                t7 = vals[6]
            except:
                t7 = 0
            try:
                t8 = vals[7]
            except:
                t8 = 0

            # btn_DWN["state"] = "normal"
            # btn_CLR["state"] = "normal"
            btn_CFG["state"] = "normal"
            btn_Disconnect["state"] = "normal"
            btn_WiFi["state"] = "normal"
            # btn_SYNC["state"] = "normal"
            # btn_TIME["state"] = "normal"
            # btn_START["state"] = "normal"

        if(s_id[0:2] == "PC" or s_id[0:2] == "AX"):
            print("Model PC or AX")
            vals = t_y.split(',')
            try:
                t1 = vals[0]
            except:
                t1 = 0
            try:
                t2 = vals[1]
            except:
                t2 = 0
            try:
                t3 = vals[2]
            except:
                t3 = 0
            try:
                t4 = vals[3]
            except:
                t4 = 0
            try:
                t5 = vals[4]
            except:
                t5 = 0
            try:
                t6 = vals[5]
            except:
                t6 = 0

            btn_DWN["state"] = "normal"
            btn_CLR["state"] = "normal"
            btn_CFG["state"] = "normal"
            btn_Disconnect["state"] = "normal"
            # btn_SYNC["state"] = "normal"
            btn_TIME["state"] = "normal"
            if(s_id[0:2] != "PC"):
                btn_START["state"] = "normal"
            if(s_id[0:2] != "PC"):
                btn_FLM["state"] = "normal"
        # btn_Connect["state"] = "normal"
        print("buttons active")
    else:
        print("No active COM ports found, reset the device and try again")
        btn_Connect["state"] = "normal"
        btn_Refresh["state"] = "normal"

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
        self.textbox.see(tk.END)
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

def th_ProgD():
    global th1
    w3 = tk.Toplevel(window)
    w3.title("Downloading")
    w3.geometry("400x200")
    w3.grab_set() # when you show the popup

    bar = Progressbar(w3, length=180, style='grey.Horizontal.TProgressbar', mode = 'indeterminate')
    bar.grid(column=0, row=0)
    # bar = Progressbar(w3, orient = HORIZONTAL,length = 100, mode = 'indeterminate')
    up_down = 1
    prog_i = 0
    while(th1.is_alive()):
        prog_i = prog_i + 1
        sleep(1)
        bar['value'] =prog_i*10
    w3.grab_release() # to return to normal
    w3.destroy()
    tk.messagebox.showinfo('Download','Download complete!')

def th_ProgC():
    global th1
    w3 = tk.Toplevel(window)
    w3.title("Clearing")
    w3.geometry("400x200")
    w3.grab_set() # when you show the popup

    bar = Progressbar(w3, length=180, style='grey.Horizontal.TProgressbar', mode = 'indeterminate')
    bar.grid(column=0, row=0)
    # bar = Progressbar(w3, orient = HORIZONTAL,length = 100, mode = 'indeterminate')
    up_down = 1
    prog_i = 0
    while(th1.is_alive()):
        prog_i = prog_i + 1
        sleep(1)
        bar['value'] =prog_i*10
    w3.grab_release() # to return to normal
    w3.destroy()
    tk.messagebox.showinfo('Clear','Data Erased')

def th_Download():
    global th1
    # Call work function
    MsgBox = tk.messagebox.askquestion ('Download data','Download data?',icon = 'warning')
    if(MsgBox == "yes"):
        print("Downloading data... Please wait")
        print(datetime.now())
        th1=Thread(target=Data_Download)
        th2 = Thread(target = th_ProgD)

        # w3 = tk.Toplevel(window)
        # w3.title("Downloading")
        # w3.geometry("200x200")

        th1.start()
        th2.start()

def th_Clear():
    # # Call work function
    # t2=Thread(target=Data_Clear)
    # t2.start()
    global th1
    # Call work function
    MsgBox = tk.messagebox.askquestion ('Clear data','Clear data?',icon = 'warning')
    if(MsgBox == "yes"):
        print("Clearing data... Please wait")
        th1=Thread(target=Data_Clear)
        th2 = Thread(target = th_ProgC)

        # w3 = tk.Toplevel(window)
        # w3.title("Downloading")
        # w3.geometry("200x200")

        th1.start()
        th2.start()

def Data_Download():
    global Com_Port
    if(send_msg(Com_Port,"2")):
        print("Data Downloaded")
        print(datetime.now())

def Data_Clear():
    global Com_Port
    if(send_msg(Com_Port,"3")):
        print("Data Cleared")

def Disconnect():
    global Com_Port
    if(send_msg(Com_Port,"9")):
        print("BYE")
        btn_DWN["state"] = "disabled"
        btn_CLR["state"] = "disabled"
        btn_CFG["state"] = "disabled"
        btn_Disconnect["state"] = "disabled"
        # btn_SYNC["state"] = "disabled"
        btn_TIME["state"] = "disabled"
        btn_START["state"] = "disabled"
        btn_Connect["state"] = "normal"
        btn_Refresh["state"] = "normal"

def openNewWindow():
    global s_id
    w2 = tk.Toplevel(window)
    w2.title("PhoCam configure")
    w2.geometry("200x200")

    if(s_id[0:2] == "PC" or s_id[0:2] == "AX"):
        w2.geometry("200x400")
        def set_CFG():
            if(int(l_init.get()) >= 0):
                t1 = l_init.get()
            if(int(l_dur.get()) >= 0):
                t2 = l_dur.get()
            if(int(l_lim.get()) >= 0):
                t3 = l_lim.get()
            if(int(l_delay.get()) >= 0):
                t4 = l_delay.get()
            if(int(l_light.get()) >= 0):
                t5 = l_light.get()
            if(int(l_depth.get()) >= 0):
                t6 = l_depth.get()
            if(int(l_depth.get()) >= 0):
                t7 = l_depth.get()
            if(int(l_depth.get()) >= 0):
                t8 = l_depth.get()
            t_init = "$"+str(t1)+","+str(t2)+","+str(t3)+","+str(t4)+","+str(t5)+","+str(t6)+","+"#"
            print("Sending " + t_init)
            if(send_msg(Com_Port,"4",t_init)):
                print("Configurations set")
                btn_apply["state"] = "disabled"

        def activate_apply(event):
            btn_apply["state"] = "normal"

        tk.Label(w2,text ="Initial delay (seconds)").pack()
        l_init = tk.Entry(w2)
        l_init.pack()
        l_init.insert(0,t1)
        l_init.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Filming duration (seconds)").pack()
        l_dur = tk.Entry(w2)
        l_dur.pack()
        l_dur.insert(0,t2)
        l_dur.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Film limit - 0 DISABLED").pack()
        l_lim = tk.Entry(w2)
        l_lim.pack()
        l_lim.insert(0,t3)
        l_lim.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Film delay (seconds)").pack()
        l_delay = tk.Entry(w2)
        l_delay.pack()
        l_delay.insert(0,t4)
        l_delay.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Light Threshold (0 - 1024)").pack()
        l_light = tk.Entry(w2)
        l_light.pack()
        l_light.insert(0,t5)
        l_light.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Depth Threshold (metre)").pack()
        l_depth = tk.Entry(w2)
        l_depth.pack()
        l_depth.insert(0,t6)
        l_depth.bind('<Button-1>', activate_apply)

        btn_apply = tk.Button(w2,text = "Apply",command = set_CFG)
        btn_apply.pack()
        btn_apply["state"] = "disabled"

    if(s_id[0:2] == "AC"):
        w2.geometry("200x400")
        def set_CFG():
            if(int(l_init.get()) >= 0):
                t1 = l_init.get()
            if(int(l_dur.get()) >= 0):
                t2 = l_dur.get()
            if(int(l_lim.get()) >= 0):
                t3 = l_lim.get()
            if(int(l_delay.get()) >= 0):
                t4 = l_delay.get()
            if(int(l_wTh.get()) >= 0):
                t5 = l_wTh.get()
            if(int(l_lTh.get()) >= 0):
                t6 = l_lTh.get()
            if(int(l_firstFilm.get()) >= 0):
                t7 = l_firstFilm.get()
            if(int(l_waterDelay.get()) >= 0):
                t8 = l_waterDelay.get()
            t_init = "$"+str(t1)+","+str(t2)+","+str(t3)+","+str(t4)+","+str(t5)+","+str(t6)+","+str(t7)+","+str(t8)+","+"#"
            print("Sending " + t_init)
            if(send_msg(Com_Port,"4",t_init)):
                print("Configurations set")
                btn_apply["state"] = "disabled"

        def activate_apply(event):
            btn_apply["state"] = "normal"

        tk.Label(w2,text ="Initial delay (seconds)").pack()
        l_init = tk.Entry(w2)
        l_init.pack()
        l_init.insert(0,t1)
        l_init.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Filming duration (seconds)").pack()
        l_dur = tk.Entry(w2)
        l_dur.pack()
        l_dur.insert(0,t2)
        l_dur.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Film limit (bouts)").pack()
        l_lim = tk.Entry(w2)
        l_lim.pack()
        l_lim.insert(0,t3)
        l_lim.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Film delay (seconds)").pack()
        l_delay = tk.Entry(w2)
        l_delay.pack()
        l_delay.insert(0,t4)
        l_delay.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Water threshold (0-1024)").pack()
        l_wTh = tk.Entry(w2)
        l_wTh.pack()
        l_wTh.insert(0,t5)
        l_wTh.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Light threshold (0-1024)").pack()
        l_lTh = tk.Entry(w2)
        l_lTh.pack()
        l_lTh.insert(0,t6)
        l_lTh.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="Initial film duration (seconds)").pack()
        l_firstFilm = tk.Entry(w2)
        l_firstFilm.pack()
        l_firstFilm.insert(0,t7)
        l_firstFilm.bind('<Button-1>', activate_apply)

        tk.Label(w2,text ="WATER delay (seconds)").pack()
        l_waterDelay = tk.Entry(w2)
        l_waterDelay.pack()
        l_waterDelay.insert(0,t8)
        l_waterDelay.bind('<Button-1>', activate_apply)

        btn_apply = tk.Button(w2,text = "Apply",command = set_CFG)
        btn_apply.pack()
        btn_apply["state"] = "disabled"

    def w2_close():
        MsgBox = tk.messagebox.askquestion ('Exit config','Are you sure you want to exit configure',icon = 'warning')
        if(MsgBox == "yes"):
            w2.destroy()
    btn_close = tk.Button(w2,text = "Close",command = w2_close)
    btn_close.pack()
    # w2.pack()


def f_quit():
    exit()

def sync_time():
    now = datetime.now()
    years = now.strftime("%Y")
    months = now.strftime("%m")
    days = now.strftime("%d")
    hours = now.strftime("%H")
    mins = now.strftime("%M")
    secs = now.strftime("%S")
    s_date = ("$" + years + "," + months + "," + days + "," + hours + "," + mins + "," + secs  + "," + "#")
    print("Sending " + s_date)
    if(send_msg(Com_Port,"5",s_date)):
        print("Time set")

b_port = 0
# Com_Port = "NA"
window = tk.Tk()
centre_window(720, 480)   # width, height
header = tk.Label(text = "Zoolog Solutions programming")
header.pack()




btn_DWN = tk.Button(window,text = "DOWNLOAD DATA",command = th_Download)# Data_Download)
btn_DWN.pack()
btn_DWN.place(x=10,y=120)
btn_DWN["state"] = "disabled"

def set_time():
    w2 = tk.Toplevel(window)
    w2.title("PhoCam configure")
    w2.geometry("200x200")
    w2.grab_set()
    def set_CFG():
        icnt = 0

        if(len(lY.get()) >= 0):
            YY = lY.get()
            try:
                YY = int(YY)
            except:
                pass
            if(type(YY) == int):
                icnt = icnt + 1
        if(len(lm.get()) >= 0):
            mm = lm.get()
            try:
                mm = int(mm)
            except:
                pass
            if(type(mm) == int):
                icnt = icnt + 1
        if(len(ld.get()) >= 0):
            dd = ld.get()
            try:
                dd = int(dd)
            except:
                pass
            if(type(dd) == int):
                icnt = icnt + 1
        if(len(lH.get()) >= 0):
            HH = lH.get()
            try:
                HH = int(HH)
            except:
                pass
            if(type(HH) == int):
                icnt = icnt + 1
        if(len(lM.get()) >= 0):
            MM = lM.get()
            try:
                MM = int(MM)
            except:
                pass
            if(type(MM) == int):
                icnt = icnt + 1
        if(len(lS.get()) >= 0):
            SS = lS.get()
            try:
                SS = int(SS)
            except:
                pass
            if(type(SS) == int):
                icnt = icnt + 1
        if(icnt == 6):

            t_time = "$"+str(YY)+","+str(mm)+","+str(dd)+","+str(HH)+","+str(MM)+","+str(SS)+","+"#"
            print("Sending " + t_time)
            if(send_msg(Com_Port,"8",t_time)):
                tk.messagebox.showinfo('PCDive','Time set')
                w2.grab_release()
                w2.destroy()
                print("Time set")
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")

    def make_label(master, x, y, h, w, stxt):
        f = tk.Frame(master, height=h, width=w)
        # f.pack_propagate(0) # don't shrink
        f.place(x=x, y=y)
        label = tk.Label(f, text = stxt)
        label.pack()
        entry = tk.Entry(master,width = len(stxt))
        entry.pack()
        # entry.insert(0," ")
        entry.place(x = x+3, y = y +20)

        def activate_apply(event):
            btn_apply["state"] = "normal"

        entry.bind('<Button-1>', activate_apply)
        return entry

    lY = make_label(w2, 10, 10, 10, 40, stxt='yyyy-')
    lm = make_label(w2, 50, 10, 10, 40, stxt='mm-')
    ld = make_label(w2, 80, 10, 10, 40, stxt='dd ')
    lH = make_label(w2, 110, 10, 10, 40, stxt='HH:')
    lM = make_label(w2, 140, 10, 10, 40, stxt='MM:')
    lS = make_label(w2, 170, 10, 10, 40, stxt='SS ')

    btn_apply = tk.Button(w2,text = "Apply",command = set_CFG)
    btn_apply.pack()
    btn_apply.place(x = 50,y = 100)
    btn_apply["state"] = "disabled"

    def w2_close():
        MsgBox = tk.messagebox.askquestion ('Exit config','Are you sure you want to exit configure',icon = 'warning')
        if(MsgBox == "yes"):
            w2.grab_release()
            w2.destroy()
    btn_close = tk.Button(w2,text = "Close",command = w2_close)
    btn_close.pack()
    btn_close.place(x = 100,y = 100)
    # w2.pack()

btn_TIME = tk.Button(window,text = "Set time",command = set_time)# Data_Download)
btn_TIME.pack()
btn_TIME.place(x=10,y=220)
btn_TIME["state"] = "disabled"


l_fn = tk.Label(window,text ="File name")
l_fn.pack()
l_fn.place(x = 165,y = 105)

l_fname = tk.Entry(window)
l_fname.pack()
l_fname.insert(0,"Download_Cache")
l_fname.place(x = 140,y = 125)

btn_CLR = tk.Button(window,text = "CLEAR DATA",command = th_Clear) #Data_Clear)
btn_CLR["state"] = "disabled"
btn_CLR.pack()
btn_CLR.place(x = 10, y = 160)

btn_QUIT = tk.Button(window,text = "QUIT",command = f_quit) #Data_Download(Com_Port)
# btn_QUIT["state"] = "disabled"
btn_QUIT.pack()
btn_QUIT.place(x = 10, y = 320)


btn_CFG = tk.Button(window,text = "Configure",command = openNewWindow)
btn_CFG.pack()
btn_CFG["state"] = "disabled"
btn_CFG.place(x = 10, y = 260)

def wifi_on():
    if(send_msg(Com_Port,"5")):
        print("WiFi on")
        btn_CAMoff["state"] = "normal"
        btn_WiFi["state"] = "disabled"

btn_WiFi = tk.Button(window,text = "WiFi on",command = wifi_on)
btn_WiFi.pack()
btn_WiFi["state"] = "disabled"
btn_WiFi.place(x = 100, y = 220)

def cam_off():
    if(send_msg(Com_Port,"6")):
        print("Cam off")
        btn_CAMoff["state"] = "disabled"
        btn_WiFi["state"] = "normal"

btn_CAMoff = tk.Button(window,text = "CAM off",command = cam_off)
btn_CAMoff.pack()
btn_CAMoff["state"] = "disabled"
btn_CAMoff.place(x = 100, y = 260)

def FLM_press():
    if(send_msg(Com_Port,"5")):
        print("FLM press")
        # btn_CAMoff["state"] = "disabled"
        # btn_WiFi["state"] = "normal"

btn_FLM = tk.Button(window,text = "FILM press",command = FLM_press)
btn_FLM.pack()
btn_FLM["state"] = "disabled"
btn_FLM.place(x = 180, y = 260)


btn_Disconnect = tk.Button(window,text = "Disconnect",command = Disconnect)
btn_Disconnect.pack()
btn_Disconnect.place(x = 130, y = 60)
btn_Disconnect["state"] = "disabled"

def fStart():
    if(send_msg(Com_Port,"8")):
        tk.messagebox.showinfo('PCDive','Logger started')
        print("Logger started")
        btn_DWN["state"] = "disabled"
        btn_CLR["state"] = "disabled"
        btn_CFG["state"] = "disabled"
        btn_Disconnect["state"] = "disabled"
        # btn_SYNC["state"] = "disabled"
        btn_START["state"] = "disabled"
        btn_Connect["state"] = "disabled"

btn_START = tk.Button(window,text = "START!",command = fStart,height = 10, width = 10)
# btn_START.pack()
# btn_START.place(x = 150, y = 260)
# btn_START["state"] = "disabled"

l_com = tk.Label(window,text = "COM port")
l_com.pack()
l_com.place(x = 50,y = 10)

cb = ttk.Combobox(window, values=List_COM_ports.serial_ports())
cb.pack()
cb.place(x=20,y=30)
# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)

btn_Connect = tk.Button(window,text = "Connect COM",command = connect)
btn_Connect.pack()
btn_Connect.place(x = 30, y = 60)
btn_Connect["state"] = "disabled"

def Refresh():
    global cb
    cb.destroy()
    cb = ttk.Combobox(window, values=List_COM_ports.serial_ports())
    cb.pack()
    cb.place(x=20,y=30)
    # assign function to combobox
    cb.bind('<<ComboboxSelected>>', on_select)

btn_Refresh = tk.Button(window,text = "Refresh",command = Refresh)
btn_Refresh.pack()
btn_Refresh.place(x = 190, y = 30)

t = tk.Text(width = 35,height = 20)
t.pack()
t.place(x = 350,y = 50)
# create instance of file like object
pl = PrintLogger(t)
# replace sys.stdout with our object
sys.stdout = pl
print("Please select a COM Port to start")
window.mainloop()
