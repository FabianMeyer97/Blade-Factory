# -*- coding: utf-8 -*-
"""
Main Window
"""

from tkinter import *
import main_do
import threading as th
import numpy as np

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
    
    
lblTemp = Label(window, text="Aktuelle Heizplattentemp in °C:")
lblTime = Label(window, text="Verstrichende Zeit in Sekunden:")
lblamax= Label(window, text="a_max:")
lblamin = Label(window, text="a_min:")
lblTmax = Label(window, text="T_max:")
lblPlus = Label(window, text="wenn + X °C:")
lblMinus = Label(window, text="wenn - X °C:")
btnUpdate = Button(window, text="Update", command=clicked)
btnEnd = Button(window, text="Stop", command=endMeasurement)

lblTemp.grid(column=0, row=0)
lblTime.grid(column=0, row=1)
lblamax.grid(column=0, row=2)
lblamin.grid(column=0, row=3)
lblTmax.grid(column=0, row=4)
lblPlus.grid(column=0, row=5)
lblMinus.grid(column=0, row=6)
btnUpdate.grid(column=2, row=0)
btnEnd.grid(column=0, row=7)

txtTemp = Entry(window,width=10)

txtTemp.grid(column=1, row=0)

print("do_once()")
global q, start, slicer, oldslice, plus
q, start, slicer, oldslice, plus = main_do.do_once()
starttime = None

def update():
    
    global do_continue, q, start, slicer, oldslice, plus, starttime
    #global u_ges, alpha_ges
    if do_continue == True:
        print("do_process()")
        q, slicer, oldslice, plus, starttime = main_do.do_process(q, start, slicer, oldslice, plus, starttime)
        print("finished")
        
        lblTime.configure(text= main_do.get_clock(slicer))
        lblTmax.configure(text= "T_max: "+main_do.get_T_max(slicer) )
        lblamax.configure(text= "a_max: "+main_do.get_a_max(slicer) )
        lblamin.configure(text= "a_min: "+main_do.get_a_min(slicer) )
        lblPlus.configure(text= main_do.get_wenn_plus(slicer) )
        lblMinus.configure(text= main_do.get_wenn_minus(slicer) )
        
        T = th.Timer(1.0, update)
        T.start()
        print("go on")
        
    else:
        main_do.end_process(slicer)
        print("stopped")

T = th.Timer(1.0, update)
T.start()




window.mainloop()
