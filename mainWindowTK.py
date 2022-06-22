# -*- coding: utf-8 -*-
"""
Main Window
"""
from tkinter import *
import main_do
import threading as th
import time
import Einlesen

window = Tk()

window.title("BladeFactory")

window.geometry('700x350')

do_continue = True

def clicked():
    res = "Heizplattentemperatur: " + txtTemp.get()
    lblTemp.configure(text= res)
    
def endMeasurement():
    global do_continue
    do_continue = False
    
def update():
    global do_continue, q, start, slicer, oldslice, plus, starttime
    #global u_ges, alpha_ges
    if do_continue == True:
        print("do_process()")
        temperature = Einlesen.getTemperature(10)+60
        q, plus, starttime = main_do.do_process(q, start, plus, starttime, temperature)
        print("finished")
        
        #global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
        lblTime.configure(text= main_do.get_clock())
        lblTemp.configure(text= f"Heizplattentemperatur: {temperature-273.15:.1f} °C")
        lblTmax.configure(text= "T_max: "+main_do.get_T_max() )
        lblamax.configure(text= f"a_max: {main_do.get_a_max():.2%}")
        lblamin.configure(text= f"a_min: {main_do.get_a_min():.2%}")
        alpha_reached, alpha_reached_at, found_alpha = main_do.find_when_alpha_min()
        if found_alpha == True:
            lblAlpha80.configure(text = f"Alpha von {alpha_reached:.1%} in {alpha_reached_at} sec erreicht")    
        lblPlus.configure(text= main_do.get_wenn_plus() )
        lblMinus.configure(text= main_do.get_wenn_minus() )
        
        T = th.Timer(1.0, update)
        T.start()
        time.sleep(5.0)
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
    
    
lblTemp = Label(window, text="Heizplattentemperatur: ")
lblTime = Label(window, text="Zeit: ")
lblamax= Label(window, text="a_max:")
lblamin = Label(window, text="a_min:")
lblTmax = Label(window, text="T_max:")
lblPlus = Label(window, text="wenn + X °C:")
lblMinus = Label(window, text="wenn - X °C:")
lblAlpha80 = Label(window)
btnUpdate = Button(window, text="Update", command=clicked)
btnStart = Button(window, text="Start", command=startProcess)
btnEnd = Button(window, text="Stop", command=endMeasurement)

lblTemp.grid(column=1, row=1)
lblTime.grid(column=1, row=3)
lblamax.grid(column=1, row=4)
lblamin.grid(column=1, row=5)
lblTmax.grid(column=1, row=2)
lblPlus.grid(column=1, row=6)
lblMinus.grid(column=1, row=7)
lblAlpha80.grid(column=1, row=12)
btnUpdate.grid(column=3, row=12)
btnStart.grid(column=0, row=0)
btnEnd.grid(column=0, row=12)

txtTemp = Entry(window,width=10)
txtTemp.grid(column=2, row=12)

window.mainloop()
"""
TODO: 
      - Layout anpassen
      - Graph einbauen
          --> Eventuell neue Graphfunktion notwendig
          --> Mehrere Graphen durch Drop down menü
          --> Tabelle die die Werte ausgibt
      - Threading für mehrere parallele Berechnungen einfügen
"""    