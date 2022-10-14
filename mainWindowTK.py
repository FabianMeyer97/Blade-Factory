# -*- coding: utf-8 -*-
"""
Main Window
"""
#from tkinter import *
from tkinter import Label, Button, Checkbutton, Tk, IntVar, Entry, Spinbox, Frame, StringVar, OptionMenu
import main_do
import threading as th
import time
import Einlesen
#import wärmeleitung

# experimental:
#from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg

from matplotlib.figure import Figure
from write import testPlot
from datetime import datetime
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
    res = "Hotplate temperature: " + HeatingTempInput.get()
    lblTemp.configure(text= res)
    temperature_entered = float(HeatingTempInput.get())

def vliesButton():
    global lblVlies
    #wärmeleitung.switchH = activeCover.get()
    switchH = activeCover.get()
    main_do.set_hswitch(switchH)
    #if wärmeleitung.switchH == True:    
    if main_do.get_hswitch() == True:   
        print("vließ hinlegen")
    else:
        print("vließ wegnehmen")
    
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
            HeatingTempInput.delete(0)
            HeatingTempInput.insert(0, round(temperature)-273.15)
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
    main_do.set_T_out(EnvTempVar.get())  #  wärmeleitung.T_out = float(EnvTempVar.get())
    #wärmeleitung.u_init = float(StartTempVar.get())
    main_do.set_u_init(float(StartTempVar.get()))
    main_do.set_h_luft(float(hLuftVar.get()))
    main_do.set_alpha_start(alpha_startVar.get())
    main_do.set_fvc(float(fvcVar.get()))
    #wärmeleitung.u_left= float(HeatingTempVar.get()) # unnecesary, is overwritten in regelung
    main_do.boundary1 = int(BoundaryAVar.get())
    main_do.boundary2 = int(BoundaryBVar.get())
    main_do.starttime_prefix = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    main_do.layer_composition = layeringVar.get()
    main_do.h = float(ThicknessVar.get())/1000
    main_do.ny = int(main_do.h/main_do.dy)  # quick and dirty...
    if main_do.layer_composition in ['with balsa core', 'default']:   #, 'with balsa core'
        main_do.set_layer_composition('balsa')
        #main_do.k_core = 0.06 #0.06-0.0935
        #main_do.density_core = 140
        #main_do.c_core = 2720
    if main_do.layer_composition in ['with foam core']:   #, 'with foam core'
        main_do.set_layer_composition('AirrexC70')
        #main_do.k_core = (0.031+0.056)/2  #0.031-0.056 #RANGE LAUT DATENBLATT
        #main_do.density_core = (40+250)/2  # 40-250 #RANGE LAUT DATENBLATT
        #main_do.c_core = 1200 #SCHÄTZWERT
    print(f"start recording at {main_do.starttime_prefix}")
    if activeDAQ.get() == 1:
        #print("is active")
        temperature = Einlesen.getTemperature(10, channel=int(inpDaqCh.get()))+273.15
        temperature_entered = round(temperature)-273.15
        HeatingTempInput.delete(0)
        HeatingTempInput.insert(0, round(temperature)-273.15)
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

controlFrame = Frame(window, width=400)
lControlFrame = Frame(window, width=400)

lblTempMINUS = Label(window, text = "MINUS: ")
lblMaxTempMINUS = Label(window, text = "T_max")
lblAlphaMinus = Label(window, text = "AlphaMInus")

lblTempPLUS = Label(window, text = "PLUS: ")
lblMaxTempPLUS = Label(window, text = "MaxTemp")
lblAlphaPLUS = Label(window, text = "AlphaPLUS")



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
lblAlpha80.grid(column=2, row=12)
controlFrame.grid( sticky='ew', row=14,columnspan=3,column=3)
lControlFrame.grid( sticky='ew', row=14,columnspan=3,column=0)

EnvTempFrame = Frame(controlFrame, width=100)
EnvTempLabel = Label(EnvTempFrame, text = "Env. temp. [°C]:")
EnvTempVar = StringVar(window, value='23.0')
EnvTempInput = Entry(EnvTempFrame, textvariable=EnvTempVar, width=5)
EnvTempFrame.pack()
EnvTempLabel.pack(side="left")
EnvTempInput.pack(side="left")

StartTempFrame = Frame(controlFrame, width=100)
StartTempLabel = Label(StartTempFrame, text = "Start temp. [°C]:")
StartTempVar = StringVar(window, value='38.0')
StartTempInput = Entry(StartTempFrame, textvariable=StartTempVar, width=5)
StartTempFrame.pack()
StartTempLabel.pack(side="left")
StartTempInput.pack(side="left")

HeatingTempFrame = Frame(controlFrame, width=100)
HeatingTempLabel = Label(HeatingTempFrame, text = "Heating temp. [°C]:")
HeatingTempVar   = StringVar(window, value='40.0')
HeatingTempInput = Entry(HeatingTempFrame, textvariable=HeatingTempVar, width=5)
HeatingTempBtn   = Button(HeatingTempFrame, text="Update", command=clicked)
HeatingTempFrame.pack()
HeatingTempLabel.pack(side="left")
HeatingTempInput.pack(side="left")
HeatingTempBtn.pack(side="left")

layeringFrame = Frame(controlFrame, width=100)
layeringLabel = Label(layeringFrame, text = "Layer:")
layeringOptions = ['only fibre layers','with balsa core', 'with foam core']
layeringVar = StringVar()
layeringVar.set(layeringOptions[0])
def layering_selected(choice):
    choice = layeringVar.get()
    print(choice)
layeringMenu = OptionMenu(layeringFrame, layeringVar, *layeringOptions, command=layering_selected)
layeringFrame.pack()
layeringLabel.pack(side="left")
layeringMenu.pack(side="left")
layeringMenu.config(width=15)

BoundaryAFrame = Frame(controlFrame, width=100)
BoundaryALabel = Label(BoundaryAFrame, text = "Boundary 1 [mm]:") # must be int
BoundaryAVar = StringVar(window, value='7')
BoundaryAInput = Entry(BoundaryAFrame, textvariable=BoundaryAVar, width=5)
BoundaryAFrame.pack()
BoundaryALabel.pack(side="left")
BoundaryAInput.pack(side="left")

BoundaryBFrame = Frame(controlFrame, width=100)
BoundaryBLabel = Label(BoundaryBFrame, text = "Boundary 2 [mm]:") #must be int
BoundaryBVar = StringVar(window, value='40')
BoundaryBInput = Entry(BoundaryBFrame, textvariable=BoundaryBVar, width=5)
BoundaryBFrame.pack()
BoundaryBLabel.pack(side="left")
BoundaryBInput.pack(side="left")

ThicknessFrame = Frame(controlFrame, width=100)
ThicknessLabel = Label(ThicknessFrame, text = "Thickness [mm]:")
ThicknessVar = StringVar(window, value='50') # can be float
ThicknessInput = Entry(ThicknessFrame, textvariable=ThicknessVar, width=5)
ThicknessFrame.pack()
ThicknessLabel.pack(side="left")
ThicknessInput.pack(side="left")

hLuftFrame = Frame(lControlFrame, width=100)
hLuftLabel = Label(hLuftFrame, text = "hAir:")
hLuftVar = StringVar(window, value='3.0') # can be float
hLuftInput = Entry(hLuftFrame, textvariable=hLuftVar, width=5)
hLuftFrame.pack()
hLuftLabel.pack(side="left")
hLuftInput.pack(side="left")

fvcFrame = Frame(lControlFrame, width=100)
fvcLabel = Label(fvcFrame, text = "fiber volume content:")
fvcVar = StringVar(window, value='0.55')
fvcInput = Entry(fvcFrame, textvariable=fvcVar, width=5)
fvcFrame.pack()
fvcLabel.pack(side="left")
fvcInput.pack(side="left")

alpha_startFrame = Frame(lControlFrame, width=100)
alpha_startLabel = Label(alpha_startFrame, text = "alphaStart:")
alpha_startVar = StringVar(window, value='0.1') # can be float
alpha_startInput = Entry(alpha_startFrame, textvariable=alpha_startVar, width=5)
alpha_startFrame.pack()
alpha_startLabel.pack(side="left")
alpha_startInput.pack(side="left")

DAQChFrame = Frame(lControlFrame, width=100)
lblDaqCh = Label(DAQChFrame, text="DAQ Channel: ") # kein Vließ abgelegt
inpDaqCh = Spinbox(DAQChFrame, from_=0, to=9, width=2)
lblDaqCh.pack(side="left")
inpDaqCh.pack(side="left")
DAQChFrame.pack()

activeDAQ = IntVar()
activeCover = IntVar()
cbAutoInput = Checkbutton(lControlFrame, text='DAQ Input',variable=activeDAQ, onvalue=1, offvalue=0)
cbCover = Checkbutton(lControlFrame, text='Cover',variable=activeCover, onvalue=True, offvalue=False, command=vliesButton)
cbAutoInput.pack() #.grid(column=1, row=12)
cbCover.pack() #grid(column=3, row=13)
## self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

StartStopFrame = Frame(lControlFrame, width=100)
btnStart = Button(StartStopFrame, text="Start", command=startProcess)
btnEnd = Button(StartStopFrame, text="Stop", command=endMeasurement)
btnStart.pack(side="left") ##grid(column=0, row=11)
btnEnd.pack(side="left") #grid(column=0, row=12)
StartStopFrame.pack()

window.mainloop()

"""
TODO: 
          --> Mehrere Graphen durch Drop down menü
          --> Tabelle die die Werte ausgibt
      - Threading für mehrere parallele Berechnungen einfügen
"""    