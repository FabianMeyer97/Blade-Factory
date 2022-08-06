# -*- coding: utf-8 -*-
"""
Main Window
"""
#from tkinter import *
from tkinter import Label, Button, Checkbutton, Tk, IntVar, Entry, Spinbox, Frame
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
temperature_entered = 40

window = Tk()

window.title("BladeFactory")

window.geometry('650x750')

matplotlib.rcParams['interactive'] = False

#experimental:
# Use TkAgg
figure, main_do.matplotax = plt.subplots()
main_do.matplotfigure = figure
# Add a canvas widget to associate the figure with canvas
main_do.matplotcanvas = FigureCanvasTkAgg(figure, window)
main_do.matplotcanvas.get_tk_widget().grid(row=15, column=0, columnspan=6)
# improve: https://stackoverflow.com/questions/30774281/update-matplotlib-plot-in-tkinter-gui
#

do_continue = True

def clicked():
    global temperature_entered
    res = "Hotplate temperature: " + txtTemp.get()
    lblTemp.configure(text= res)
    temperature_entered = float(txtTemp.get())

def vliesButton():
    global lblVlies
    #wärmeleitung.switchH = not wärmeleitung.switchH
    wärmeleitung.switchH = activeCover.get()
    if wärmeleitung.switchH == True:    
        print("vließ hinlegen")
        #lblVlies.config(text = "Vließ hingelegt")
    else:
        print("vließ wegnehmen")
        #lblVlies.config(text = "Vließentfernt")
    
def endMeasurement():
    global do_continue
    do_continue = False
    
def update():
    global do_continue, q, start, slicer, oldslice, plus, starttime, temperature_entered
    #global u_ges, alpha_ges
    if do_continue == True:
        print("do_process()")
        if activeDAQ.get() == 1:
            #print("is active")
            #print("channel")
            #print(inpDaqCh.get())
            #print(type(inpDaqCh.get()))
            temperature = Einlesen.getTemperature(10, channel=int(inpDaqCh.get()))+273.15
            temperature_entered = round(temperature)-273.15
            txtTemp.delete(0)
            txtTemp.insert(0, round(temperature)-273.15)
        else:
            print("is not active")
            temperature = temperature_entered +273.15
            print(temperature)
        q, plus, starttime = main_do.do_process(q, start, starttime, temperature) #, plus
        #print("finished")
        
        #global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
        #lblTime.configure(text= main_do.get_clock())
        lblTemp.configure(text= f"Heizplattentemperatur: {temperature-273.15:.1f} °C")
        lblTmax.configure(text= f"T_max: {main_do.get_T_max():.1f} °C")
        #lblamax.configure(text= f"α_max: {main_do.get_a_max():.2%} °C")
        lblamin.configure(text= f"({main_do.get_a_min():.2%}, {main_do.get_a_max():.2%})")
        alpha_reached, alpha_reached_at, found_alpha = main_do.find_when_alpha_min()
        if found_alpha == True:
            lblAlpha80.configure(text = f"Alpha von {alpha_reached:.2%} in {alpha_reached_at} sec erreicht")
            
        lblMaxTempMINUS.configure(text=f"T_max: {main_do.get_minus():.1f}")
        lblMaxTempPLUS.configure(text=f"T_max: {main_do.get_plus():.1f}")
        lblTempPLUS.configure(text=f"{temperature+main_do.get_delta_plus()-273.15:.1f} °C (+ {main_do.get_delta_plus():.1f} °C)")
        lblTempMINUS.configure(text=f"{temperature-main_do.get_delta_plus()-273.15:.1f} °C (- {main_do.get_delta_plus():.1f} °C)")
        lblPlus.configure(text= main_do.get_wenn_plus() )
        lblMinus.configure(text= main_do.get_wenn_minus() )
        lblAlphaPLUS.configure(text=f"({main_do.get_alpha_min_PLUS():.2%},{main_do.get_alpha_max_PLUS():.2%})")
        lblAlphaMinus.configure(text=f"({main_do.get_alpha_min_MINUS():.2%},{main_do.get_alpha_max_MINUS():.2%})")
        
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
        #print("is active")
        temperature = Einlesen.getTemperature(10, channel=int(inpDaqCh.get()))+273.15
        temperature_entered = round(temperature)-273.15
        txtTemp.delete(0)
        txtTemp.insert(0, round(temperature)-273.15)
    else:
        print("is not active")
        temperature = temperature_entered +273.15
        print(temperature)
    q, start, plus = main_do.do_once(temperature)
    global starttime
    starttime = None
    #q = -1
    T = th.Timer(1.0, update)
    T.start()
    
lblTemp = Label(window, text="Heizplattentemperatur: ")
lblTime = Label(window, text="Zeit: ")
lblamax= Label(window, text="Aushärtegrad (α_min,α_max):")
lblamin = Label(window, text="a_min:")
lblTmax = Label(window, text="T_max:")
lblPlus = Label(window, text="wenn + X °C:")
lblMinus = Label(window, text="wenn - X °C:")
lblAlpha80 = Label(window)
#lblVlies = Label(window, text=" Vlies Platzhalter") # kein Vließ abgelegt

#updateTempFrame = Frame(window, width=150, bg="blue")
controlFrame = Frame(window, width=800)

lblTempMINUS = Label(window, text = f"MINUS: ") #hier muss noch -MINUS gegetted werden
lblMaxTempMINUS = Label(window, text = "T_max")
lblAlphaMinus = Label(window, text = "AlphaMInus")

lblTempPLUS = Label(window, text = f"PLUS: ") #hier muss noch -PLUS gegetted werden
lblMaxTempPLUS = Label(window, text = "MaxTemp")
lblAlphaPLUS = Label(window, text = "AlphaPLUS")

btnUpdate = Button(controlFrame, text="Update", command=clicked)
btnStart = Button(controlFrame, text="Start", command=startProcess)
btnEnd = Button(controlFrame, text="Stop", command=endMeasurement)
#btnVlies = Button(window, text="Vlies", command=vliesButton)


lblDaqCh = Label(controlFrame, text="DAQ Channel: ") # kein Vließ abgelegt
inpDaqCh = Spinbox(controlFrame, from_=0, to=9, width=2)

activeDAQ = IntVar()
activeCover = IntVar()
cbAutoInput = Checkbutton(controlFrame, text='DAQ Input',variable=activeDAQ, onvalue=1, offvalue=0)
cbCover = Checkbutton(controlFrame, text='Cover',variable=activeCover, onvalue=True, offvalue=False, command=vliesButton)

lblTempMINUS.grid(column=1, row=1)
lblMaxTempMINUS.grid(column=1,row=2)
lblAlphaMinus.grid(column=1,row=5)

lblTempPLUS.grid(column=3, row=1)
lblMaxTempPLUS.grid(column=3,row=2)
lblAlphaPLUS.grid(column=3,row=5)

#lblVlies.grid(column=4,row= 13)
lblTemp.grid(column=2, row=1)
#lblTime.grid(column=2, row=0)
lblamax.grid(column=2, row=4)
lblamin.grid(column=2, row=5)
lblTmax.grid(column=2, row=2)
lblPlus.grid(column=3, row=3)
lblMinus.grid(column=1, row=3)
cbAutoInput.pack(side="left") #.grid(column=1, row=12)
lblDaqCh.pack(side="left") #.grid(column=2,row=13)
inpDaqCh.pack(side="left") #grid(column=1, row=13)
lblAlpha80.grid(column=2, row=12)
#updateTempFrame.grid(column=3, row=12)
controlFrame.grid( sticky='ew', row=14,columnspan=5,)
btnStart.pack(side="left") ##grid(column=0, row=11)
btnEnd.pack(side="left") #grid(column=0, row=12)
#btnVlies.grid(column=0, row=13)

txtTemp = Entry(controlFrame,width=10)
txtTemp.pack(side="left") #.grid(column=3, row=12)
btnUpdate.pack(side="left")#.grid(column=3, row=12)
cbCover.pack(side="left") #grid(column=3, row=13)
## self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

window.mainloop()

"""
TODO: 
          --> Mehrere Graphen durch Drop down menü
          --> Tabelle die die Werte ausgibt
      - Threading für mehrere parallele Berechnungen einfügen
"""    