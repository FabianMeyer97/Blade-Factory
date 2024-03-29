# -*- coding: utf-8 -*-
"""
Main Window
"""
#from tkinter import *
from tkinter import Label, Button, Checkbutton, Tk, IntVar, Entry, Spinbox, Frame, StringVar, OptionMenu
import main_do 
# sollte Klasse sein, mit Variabler für Kanal
# verschiedene Instanzn in Liste speichern (heatingPlates)
import threading as th
import time
import Einlesen
#import wärmeleitung
import numpy as np

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

heatingPlates = []
heatingPlate0 = main_do.heatingPlateSimulation(0)
heatingPlate1 = main_do.heatingPlateSimulation(1)
heatingPlates.append( heatingPlate0 )
heatingPlates.append( heatingPlate1 )
heatingPlates[0].lastTemperature = 273.15+40
heatingPlates[1].lastTemperature = 273.15+40

window = Tk()

window.title("BladeFactory")

window.geometry('650x750')

matplotlib.rcParams['interactive'] = False

#experimental:
# Use TkAgg
#figure, main_do.matplotax = plt.subplots()
#main_do.matplotfigure = figure
heatingPlate0.figure, heatingPlate0.matplotax = plt.subplots()
heatingPlate0.matplotfigure = heatingPlate0.figure
heatingPlate1.figure, heatingPlate1.matplotax = plt.subplots()  # heatingPlate0.figure, heatingPlate0.matplotax
heatingPlate1.matplotfigure = heatingPlate1.figure   # heatingPlate0.matplotfigure #
#heatingPlate0 heatingPlate1
# Add a canvas widget to associate the figure with canvas
#main_do.matplotcanvas = FigureCanvasTkAgg(figure, window)
#main_do.matplotcanvas.get_tk_widget().grid(row=15, column=0, columnspan=6)
heatingPlate0.matplotcanvas = FigureCanvasTkAgg(heatingPlate0.figure, window)
heatingPlate0.matplotcanvas.get_tk_widget().grid(row=15, column=0, columnspan=6)
heatingPlate1.matplotcanvas = FigureCanvasTkAgg(heatingPlate1.figure, window)  # heatingPlate0.matplotcanvas #
heatingPlate1.matplotcanvas.get_tk_widget().grid(row=15, column=6, columnspan=7)
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
    #main_do.set_hswitch(switchH) 
    heatingPlate0.set_hswitch(switchH)  #
    heatingPlate1.set_hswitch(switchH)  # sollte separat sein !!!!!!!!!!!!!!!!!!!!!!!!!!!1
    #if wärmeleitung.switchH == True:    
    if heatingPlate0.get_hswitch() == True:   
        print("vließ 0 hinlegen")
    else:
        print("vließ 0 wegnehmen")
    if heatingPlate1.get_hswitch() == True:   
        print("vließ 1 hinlegen")
    else:
        print("vließ 1 wegnehmen")
    
def endMeasurement():
    global do_continue
    do_continue = False
    
def update():
    global do_continue, q, start, slicer, oldslice, plus, starttime, temperature_entered  # most of them not needed
    if do_continue == True:
        print("do_process()")
        if activeDAQ.get() == 1:
            #temperature = Einlesen.getTemperature(10, channel=int(inpDaqCh.get()))+273.15
            temperatures = Einlesen.getTemperature(10) ####
            while sum(np.isnan(np.array(temperatures)))>1 : # >1 weil momentan drei felder, eines ist nan
                temperatures = Einlesen.getTemperature(10)
            
            temperatures = [x+273.15 for x in temperatures]
            chTemperature = temperatures[int(inpDaqCh.get())]
            temperature_entered = round(chTemperature)-273.15
            HeatingTempInput.delete(0)
            HeatingTempInput.insert(0, temperature_entered)
        else:
            chTemperature = temperature_entered +273.15
            #lastTemperatures
            temperatures = [heatingPlates[0].lastTemperature, heatingPlates[1].lastTemperature] ########################### 222222222222222222222222222222222222222
            #temperatures = [chTemperature]
            temperatures[int(inpDaqCh.get())] = chTemperature
            print("temperature for channel "+str(inpDaqCh.get())+" entered: "+str(chTemperature))
        #q, plus, starttime = main_do.do_process(q, start, starttime, temperatures, int(inpDaqCh.get())) #, plus   ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        heatingPlate0.q, heatingPlate0.plus, heatingPlate0.starttime = heatingPlate0.do_process(heatingPlate0.q, heatingPlate0.start, heatingPlate0.starttime, temperatures[0], 0, do_plot=True, matplotfigure=heatingPlate0.matplotfigure, matplotax=heatingPlate0.matplotax) #, plus   ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        heatingPlate1.q, heatingPlate1.plus, heatingPlate1.starttime = heatingPlate1.do_process(heatingPlate1.q, heatingPlate1.start, heatingPlate1.starttime, temperatures[1], 1, do_plot=True, matplotfigure=heatingPlate1.matplotfigure, matplotax=heatingPlate1.matplotax) #, plus   ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print("finished")
        
        #global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
        #lblTime.configure(text= main_do.get_clock())
        lblTemp.configure(text= f"Heizplattentemperatur: {chTemperature-273.15:.1f} °C")
        #lblTmax.configure(text= f"T_max: {main_do.get_T_max():.1f} °C") #int(inpDaqCh.get())  heatingPlates[int(inpDaqCh.get())]
        lblTmax.configure(text= f"T_max: {heatingPlates[int(inpDaqCh.get())].get_T_max():.1f} °C") #int(inpDaqCh.get())  heatingPlates[int(inpDaqCh.get())]
        #lblamax.configure(text= f"α_max: {main_do.get_a_max():.2%} °C")
        #lblamin.configure(text= f"({main_do.get_a_min():.2%}, {main_do.get_a_max():.2%})")
        lblamin.configure(text= f"({heatingPlates[int(inpDaqCh.get())].get_a_min():.2%}, {heatingPlates[int(inpDaqCh.get())].get_a_max():.2%})")
        #alpha_reached, alpha_reached_at, found_alpha = main_do.find_when_alpha_min()
        alpha_reached, alpha_reached_at, found_alpha = heatingPlates[int(inpDaqCh.get())].find_when_alpha_min()
        if found_alpha == True:
            lblAlpha80.configure(text = f"Alpha von {alpha_reached:.2%} in {alpha_reached_at} sec erreicht")
            
        #lblMaxTempMINUS.configure(text=f"T_max: {main_do.get_minus():.1f}")
        #lblMaxTempPLUS.configure(text=f"T_max: {main_do.get_plus():.1f}")
        #lblTempPLUS.configure(text=f"{chTemperature+main_do.get_delta_plus()-273.15:.1f} °C (+ {main_do.get_delta_plus():.1f} °C)")
        #lblTempMINUS.configure(text=f"{chTemperature-main_do.get_delta_plus()-273.15:.1f} °C (- {main_do.get_delta_plus():.1f} °C)")
        #lblPlus.configure(text= main_do.get_wenn_plus() )
        #lblMinus.configure(text= main_do.get_wenn_minus() )
        #lblAlphaPLUS.configure(text=f"({main_do.get_alpha_min_PLUS():.2%},{main_do.get_alpha_max_PLUS():.2%})")
        #lblAlphaMinus.configure(text=f"({main_do.get_alpha_min_MINUS():.2%},{main_do.get_alpha_max_MINUS():.2%})")
        lblMaxTempMINUS.configure(text=f"T_max: {heatingPlates[int(inpDaqCh.get())].get_minus():.1f}")
        lblMaxTempPLUS.configure(text=f"T_max: {heatingPlates[int(inpDaqCh.get())].get_plus():.1f}")
        lblTempPLUS.configure(text=f"{chTemperature+heatingPlates[int(inpDaqCh.get())].get_delta_plus()-273.15:.1f} °C (+ {heatingPlates[int(inpDaqCh.get())].get_delta_plus():.1f} °C)")
        lblTempMINUS.configure(text=f"{chTemperature-heatingPlates[int(inpDaqCh.get())].get_delta_plus()-273.15:.1f} °C (- {heatingPlates[int(inpDaqCh.get())].get_delta_plus():.1f} °C)")
        lblPlus.configure(text= heatingPlates[int(inpDaqCh.get())].get_wenn_plus() )
        lblMinus.configure(text= heatingPlates[int(inpDaqCh.get())].get_wenn_minus() )
        lblAlphaPLUS.configure(text=f"({heatingPlates[int(inpDaqCh.get())].get_alpha_min_PLUS():.2%},{heatingPlates[int(inpDaqCh.get())].get_alpha_max_PLUS():.2%})")
        lblAlphaMinus.configure(text=f"({heatingPlates[int(inpDaqCh.get())].get_alpha_min_MINUS():.2%},{heatingPlates[int(inpDaqCh.get())].get_alpha_max_MINUS():.2%})")
        
        T = th.Timer(1.0, update)
        T.start()
        #time.sleep(5.0)
        print("go on")
        
    else:
        #main_do.end_process()
        heatingPlates[0].end_process(do_plot=True, matplotfigure=heatingPlate0.matplotfigure, matplotax=heatingPlate0.matplotax)
        heatingPlates[1].end_process(do_plot=True, matplotfigure=heatingPlate1.matplotfigure, matplotax=heatingPlate1.matplotax)
        print("stopped")

def startProcess():
    ### ACHTUNG ###
    #
    # evtl. startzeitpunkt für ch1 vo vornherein festlegen
    #
    # aufbauarten erstmal hier im code für beide ch festlegen
    #
    # dicke im code festlegen 
    #
    print("do_once()")
    global q, start, slicer, oldslice, plus, temperature_entered  #most of them not needed
    #main_do.set_T_out(EnvTempVar.get())  #  wärmeleitung.T_out = float(EnvTempVar.get())
    heatingPlates[0].set_T_out(EnvTempVar.get())  #  wärmeleitung.T_out = float(EnvTempVar.get())  #heatingPlates[int(inpDaqCh.get())]
    heatingPlates[1].set_T_out(EnvTempVar.get())  #  wärmeleitung.T_out = float(EnvTempVar.get())  #heatingPlates[int(inpDaqCh.get())]
    #wärmeleitung.u_init = float(StartTempVar.get())
    #main_do.set_u_init(float(StartTempVar.get()))
    #main_do.set_h_luft(float(hLuftVar.get()))
    #main_do.set_alpha_start(alpha_startVar.get())
    #main_do.set_fvc(float(fvcVar.get()))
    # heatingPlates[0]
    heatingPlates[0].set_u_init(float(StartTempVar.get()))
    heatingPlates[0].set_h_luft(float(hLuftVar.get()))
    heatingPlates[0].set_alpha_start(alpha_startVar.get())
    heatingPlates[0].set_fvc(float(fvcVar.get()))
    # heatingPlates[1]
    heatingPlates[1].set_u_init(float(StartTempVar.get()))
    heatingPlates[1].set_h_luft(float(hLuftVar.get()))
    heatingPlates[1].set_alpha_start(alpha_startVar.get())
    heatingPlates[1].set_fvc(float(fvcVar.get()))
    #
    #wärmeleitung.u_left= float(HeatingTempVar.get()) # unnecesary, is overwritten in regelung
    #main_do.boundary1 = int(BoundaryAVar.get())
    #main_do.boundary2 = int(BoundaryBVar.get())
    #main_do.starttime_prefix = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    #main_do.layer_composition = layeringVar.get()
    #main_do.h = float(ThicknessVar.get())/1000
    #main_do.ny = int(main_do.h/main_do.dy)  # quick and dirty...
    #
    heatingPlates[0].boundary1 = 3 # int(BoundaryAVar.get())
    heatingPlates[0].boundary2 = 26 # int(BoundaryBVar.get())
    heatingPlates[0].starttime_prefix = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    heatingPlates[0].layer_composition = 'with foam core' #layeringVar.get()
    heatingPlates[0].h = 0.030 #float(ThicknessVar.get())/1000
    heatingPlates[0].ny = int(heatingPlates[0].h/heatingPlates[0].dy)  # quick and dirty...
    #
    heatingPlates[1].boundary1 = 3 #int(BoundaryAVar.get())
    heatingPlates[1].boundary2 = 26 #int(BoundaryBVar.get())
    heatingPlates[1].starttime_prefix = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    heatingPlates[1].layer_composition = 'only fibre layers' #layeringVar.get()
    heatingPlates[1].h = 0.034  #float(ThicknessVar.get())/1000
    heatingPlates[1].ny = int(heatingPlates[1].h/heatingPlates[1].dy)  # quick and dirty...
    #
    #if main_do.layer_composition in ['with balsa core', 'default']:   #, 'with balsa core'
    #    main_do.set_layer_composition('balsa')
    #    #main_do.k_core = 0.06 #0.06-0.0935
    #    #main_do.density_core = 140
    #    #main_do.c_core = 2720
    #if main_do.layer_composition in ['with foam core']:   #, 'with foam core'
    #    main_do.set_layer_composition('AirrexC70')
    #    #main_do.k_core = (0.031+0.056)/2  #0.031-0.056 #RANGE LAUT DATENBLATT
    #    #main_do.density_core = (40+250)/2  # 40-250 #RANGE LAUT DATENBLATT
    #    #main_do.c_core = 1200 #SCHÄTZWERT
    #print(f"start recording at {main_do.starttime_prefix}")
    # heatingPlates[0]
    if heatingPlates[0].layer_composition in ['with balsa core', 'default']:   #, 'with balsa core'
        heatingPlates[0].set_layer_composition('balsa')
    if heatingPlates[0].layer_composition in ['with foam core']:   #, 'with foam core'
        heatingPlates[0].set_layer_composition('AirrexC70')
    print(f"start recording at {heatingPlates[0].starttime_prefix}")
    # heatingPlates[1]
    if heatingPlates[1].layer_composition in ['with balsa core', 'default']:   #, 'with balsa core'
        heatingPlates[1].set_layer_composition('balsa')
    if heatingPlates[1].layer_composition in ['with foam core']:   #, 'with foam core'
        heatingPlates[1].set_layer_composition('AirrexC70')
    print(f"start recording at {heatingPlates[1].starttime_prefix}")
    # 
    if activeDAQ.get() == 1:        
        temperatures = Einlesen.getTemperature(10)
        while sum(np.isnan(np.array(temperatures)))>1 : # >1 weil momentan drei felder, eines ist nan
            print("NaN in sensordata: "+str(temperatures))
            temperatures = Einlesen.getTemperature(10)
            
        temperatures = [x+273.15 for x in temperatures]
        chTemperature = temperatures[int(inpDaqCh.get())]
        temperature_entered = round(chTemperature)-273.15
        HeatingTempInput.delete(0)
        HeatingTempInput.insert(0, temperature_entered)
    else:
        print("is not active")
        chTemperature = temperature_entered +273.15
        #lastTemperatures
        temperatures = [heatingPlates[0].lastTemperature, heatingPlates[1].lastTemperature] ########################### 222222222222222222222222222222222222222
        #temperatures = [chTemperature]
        temperatures[int(inpDaqCh.get())] = chTemperature
        print("temperature for channel "+str(inpDaqCh.get())+" entered: "+str(chTemperature))
    #q, start, plus = main_do.do_once(temperatures, int(inpDaqCh.get()))  ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print("temperatures: "+str(temperatures))
    heatingPlates[0].q, heatingPlates[0].start, heatingPlates[0].plus = heatingPlates[0].do_once(temperatures[0], 0, do_plot=int(inpDaqCh.get())==0)  ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    heatingPlates[1].q, heatingPlates[1].start, heatingPlates[1].plus = heatingPlates[1].do_once(temperatures[1], 1, do_plot=int(inpDaqCh.get())==1)  ################################  einmal für ch0 einmal für ch1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    global starttime
    starttime = None
    heatingPlates[0].starttime = None
    heatingPlates[1].starttime = None
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