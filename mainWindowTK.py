# -*- coding: utf-8 -*-
"""
Main Window
"""

from tkinter import *
import main_do
import threading as th

window = Tk()

window.title("BladeFactory")

window.geometry('650x200')

do_continue = True

def clicked():
    res = "Aktuelle Heizplattentemp in °C: " + txtTemp.get()
    lblTemp.configure(text= res)
    
def endMeasurement():
    global do_continue
    do_continue = False
    
def update():
    
    global do_continue, q, start, slicer, oldslice, plus, starttime
    #global u_ges, alpha_ges
    if do_continue == True:
        print("do_process()")
        q, plus, starttime = main_do.do_process(q, start, plus, starttime)
        print("finished")
        
        #global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
        lblTime.configure(text= main_do.get_clock())
        lblTmax.configure(text= "T_max: "+main_do.get_T_max() )
        lblamax.configure(text= "a_max: "+main_do.get_a_max() )
        lblamin.configure(text= "a_min: "+main_do.get_a_min() )
        lblPlus.configure(text= main_do.get_wenn_plus() )
        lblMinus.configure(text= main_do.get_wenn_minus() )
        
        T = th.Timer(1.0, update)
        T.start()
        print("go on")
        
    else:
        main_do.end_process()
        print("stopped")

def startProcess():
    print("do_once()")
    global q, start, slicer, oldslice, plus
    q, start, plus = main_do.do_once()
    global starttime
    starttime = None
    #q = -1
    T = th.Timer(1.0, update)
    T.start()    
    
lblTemp = Label(window, text="Aktuelle Heizplattentemp in °C:")
lblTime = Label(window, text="Verstrichende Zeit in Sekunden:")
lblamax= Label(window, text="a_max:")
lblamin = Label(window, text="a_min:")
lblTmax = Label(window, text="T_max:")
lblPlus = Label(window, text="wenn + X °C:")
lblMinus = Label(window, text="wenn - X °C:")
btnUpdate = Button(window, text="Update", command=clicked)
btnStart = Button(window, text="Start", command=startProcess)
btnEnd = Button(window, text="Stop", command=endMeasurement)

lblTemp.grid(column=1, row=0)
lblTime.grid(column=1, row=1)
lblamax.grid(column=1, row=2)
lblamin.grid(column=1, row=3)
lblTmax.grid(column=1, row=4)
lblPlus.grid(column=1, row=5)
lblMinus.grid(column=1, row=6)
btnUpdate.grid(column=3, row=0)
btnStart.grid(column=0, row=0)
btnEnd.grid(column=1, row=7)

txtTemp = Entry(window,width=10)

txtTemp.grid(column=2, row=0)

window.mainloop()

"""
TODO: - a-Max a min anpassen
      - Layout anpassen
      - Graph einbauen
          --> Eventuell neue Graphfunktion notwendig
    
"""    