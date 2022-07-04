# -*- coding: utf-8 -*-
"""
Main Window
"""
#from tkinter import *
from tkinter import Label, Button, Checkbutton, Tk, IntVar, Entry
import main_do
import threading as th
import time
import Einlesen
import wärmeleitung

# experimental:
#from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from write import testPlot
#

global temperature_entered
temperature_entered = 123
#        if activeDAQ.get() == 1:
#            temperature = Einlesen.getTemperature(10)+60
#            temperature_entered = temperature
#            txtTemp.insert(0, temperature)
#            temperature = 100.0
#        else:
#            temperature = temperature_entered
#            temperature = 100.0
window = Tk()

window.title("BladeFactory")

window.geometry('500x550')

matplotlib.rcParams['interactive'] = False

#experimental:
# Use TkAgg
figure, main_do.matplotax = plt.subplots()
# Add a canvas widget to associate the figure with canvas
main_do.matplotcanvas = FigureCanvasTkAgg(figure, window)
main_do.matplotcanvas.get_tk_widget().grid(row=15, column=0, columnspan=6)
# improve: https://stackoverflow.com/questions/30774281/update-matplotlib-plot-in-tkinter-gui
#

do_continue = True

def clicked():
    global temperature_entered
    res = "Heizplattentemperatur: " + txtTemp.get()
    lblTemp.configure(text= res)
    temperature_entered = float(txtTemp.get())

def vliesButton():
    global lblVlies
    wärmeleitung.switchH = not wärmeleitung.switchH
    if wärmeleitung.switchH == True:    
        print("vließ hinlegen")
        lblVlies.config(text = "Vließ hingelegt")
    else:
        print("vließ wegnehmen")
        lblVlies.config(text = "Vließentfernt")
    
def endMeasurement():
    global do_continue
    do_continue = False
    
def update():
    global do_continue, q, start, slicer, oldslice, plus, starttime, temperature_entered
    #global u_ges, alpha_ges
    if do_continue == True:
        print("do_process()")
        if activeDAQ.get() == 1:
            print("is active")
            temperature = Einlesen.getTemperature(10)+60
            temperature_entered = round(temperature)-273.15
            txtTemp.delete(0)
            txtTemp.insert(0, round(temperature)-273.15)
        else:
            print("is not active")
            temperature = temperature_entered +273.15
            print(temperature)
        #temperature = Einlesen.getTemperature(10)+60
        q, plus, starttime = main_do.do_process(q, start, plus, starttime, temperature)
        print("finished")
        
        #global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
        lblTime.configure(text= main_do.get_clock())
        lblTemp.configure(text= f"Heizplattentemperatur: {temperature-273.15:.1f} °C")
        lblTmax.configure(text= f"T_max: {main_do.get_T_max():.1f}")
        lblamax.configure(text= f"a_max: {main_do.get_a_max():.2%}")
        lblamin.configure(text= f"a_min: {main_do.get_a_min():.2%}")
        alpha_reached, alpha_reached_at, found_alpha = main_do.find_when_alpha_min()
        if found_alpha == True:
            lblAlpha80.configure(text = f"Alpha von {alpha_reached:.1%} in {alpha_reached_at} sec erreicht")
            
        lblMaxTempMINUS.configure(text="T_max: " + main_do.get_minus())
        #lblPlus.configure(text= main_do.get_wenn_plus() )
        #lblMinus.configure(text= main_do.get_wenn_minus() )
        
        T = th.Timer(1.0, update)
        T.start()
        #time.sleep(5.0)
        print("go on")
        
    else:
        main_do.end_process()
        print("stopped")

def startProcess():
    print("do_once()")
    global q, start, slicer, oldslice, plus, temperature_entered
    if activeDAQ.get() == 1:
        print("is active")
        temperature = Einlesen.getTemperature(10)+60
        temperature_entered = round(temperature)-273.15
        txtTemp.delete(0)
        txtTemp.insert(0, round(temperature)-273.15)
    else:
        print("is not active")
        temperature = temperature_entered +273.15
        print(temperature)
    #temperature = Einlesen.getTemperature(10)+60
    q, start, plus = main_do.do_once(temperature)
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
lblVlies = Label(window, text=" ") # kein Vließ abgelegt

lblTempMINUS = Label(window, text = f"MINUS: ") #hier muss noch -MINUS gegetted werden
lblMaxTempMINUS = Label(window, text = "T_max")
lblAlphaMinus = Label(window, text = "AlphaMInus")

lblTempPLUS = Label(window, text = f"PLUS: ") #hier muss noch -PLUS gegetted werden
lblMaxTempPLUS = Label(window, text = "MaxTemp")
lblAlphaPLUS = Label(window, text = "AlphaPLUS")


btnUpdate = Button(window, text="Update", command=clicked)
btnStart = Button(window, text="Start", command=startProcess)
btnEnd = Button(window, text="Stop", command=endMeasurement)
btnVlies = Button(window, text="Vlies", command=vliesButton)

activeDAQ = IntVar()
cbAutoInput = Checkbutton(window, text='DAQ Input',variable=activeDAQ, onvalue=1, offvalue=0)

lblTempMINUS.grid(column=1, row=2)
lblMaxTempMINUS.grid(column=1,row=3)
lblAlphaMinus.grid(column=1,row=4)

lblTempPLUS.grid(column=3, row=2)
lblMaxTempPLUS.grid(column=3,row=3)
lblAlphaPLUS.grid(column=3,row=4)

lblVlies.grid(column=1,row= 13)
lblTemp.grid(column=2, row=2)
lblTime.grid(column=2, row=1)
lblamax.grid(column=2, row=4)
lblamin.grid(column=2, row=5)
lblTmax.grid(column=2, row=3)
lblPlus.grid(column=2, row=6)
lblMinus.grid(column=2, row=7)
cbAutoInput.grid(column=1, row=12)
lblAlpha80.grid(column=2, row=12)
btnUpdate.grid(column=4, row=12)
btnStart.grid(column=0, row=0)
btnEnd.grid(column=0, row=12)
btnVlies.grid(column=0, row=13)

txtTemp = Entry(window,width=10)
txtTemp.grid(column=3, row=12)

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