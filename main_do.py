"""
Main Datei

"""
import numpy as np
import wärmeleitung as w
import write
import reg
import time
import Einlesen as e
import keyboard
#import tkinter as tk
import datetime

global slicer, oldslice
global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus

h = 0.013 #[m]
dy = 0.001#[m]
dt = 1
ny = int(h/dy)
dy2 = dy*dy
#Hier boundaries eingeben [in mm]:
boundary1 = int(7)
boundary2 = int((6.5+31.5))
nsteps1 = Sekunden =  int(10*60*60)
stepsprorechnung = int(1200)
nsteps = int(Sekunden/dt)

maxerlaubteTemperatur = 40 +273.15

plus = 20

documentation = []
np.array(documentation)

# def update_clock():
#     # get current time as text
#     current_time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    
#     lab.config(text=current_time)
#     #lab['text'] = current_time 
#     root.after(1000, update_clock) 
def set_clock():
    global str_clock
    str_clock = "Verstrichende Zeit in Sekunden: " + str(slicer)
    
def get_clock():
    global str_clock
    return str_clock

def set_T_max():
    global u_ges
    global str_T_max
    str_T_max = str(np.amax(u_ges[slicer:])-273.15) 

def get_T_max():
    global str_T_max
    return str_T_max

def set_a_max():
    global alpha_ges
    global str_a_max
    str_a_max = str(np.amax(alpha_ges[slicer]))

def get_a_max():
    global str_a_max
    return str_a_max

def set_a_min():
    global alpha_ges
    global str_a_min
    str_a_min = str(np.amin(alpha_ges[slicer]))

def get_a_min():
    global str_a_min
    return str_a_min

def set_wenn_plus():
    global plus, u_ges_PLUS, slicer
    global str_wenn_plus
    result = np.where(u_ges_PLUS == np.amax(u_ges_PLUS[slicer:]))
    str_wenn_plus = "wenn + "+str(int(plus))+ "°C: " + str(np.amax(u_ges_PLUS[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm."

def get_wenn_plus():
    global str_wenn_plus
    return str_wenn_plus

def set_wenn_minus():
    global plus, u_ges_MINUS, slicer
    global str_wenn_minus
    result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[slicer:]))
    str_wenn_minus = "wenn - "+str(int(plus))+ "°C: " + str(np.amax(u_ges_MINUS[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm."

def get_wenn_minus():
    global str_wenn_minus
    return str_wenn_minus

"""
while True:
    try:     
        eingegeben1 = int(input("Aktuelle Heizplattentemp in °C: "))+273.15
        #eingegeben1 = e.getTemperature(10)
    except ValueError:
        print("Keine Integer-Zahl eingegeben")
    else:
        if (eingegeben1 > 0+273.15 and eingegeben1 < 150+273.15):
            break   
        print("Wert zu hoch oder zu gering!")
"""
def do_once():
    global u_ges, alpha_ges, dadt_ges, u, u0
    global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
    global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
    global plus#, slicer, oldslice, q
    global nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung
    global documentation
    global slicer, oldslice
    eingegeben1 = e.getTemperature(10)   
    documentation.append((0,eingegeben1))
    start = time.time()
    u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung1(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung)
    u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung1_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
    u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung1_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
    plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
    if plus < 0:
        plus = 0
    print(plus)
    
    #write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)
    
    
    slicer = 0
    oldslice = 0
    q = -1
    return q, start, plus
    
#while True:  
def do_process(q, start, plus, starttime):
    global u_ges, alpha_ges, dadt_ges, u, u0
    global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
    global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
    #global plus#, slicer, oldslice, q
    global nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung
    global documentation
    global slicer, oldslice
    q += 1  
    
    eingegeben = e.getTemperature(10)
    endtime = time.time()
    
    if q == 0:
        dif1 = int(endtime-start)
        #dif1 = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(dif1))
        slicer += dif1 
    else: 
        """                
        if eingegeben == 555+273.15:            
             w.switchH = not w.switchH
        """
        """
        if keyboard.read_key() == "p" or keyboard.read_key() == "f":            #Hier wird auf Eingabe gewartet tkinter hat wohl eine Funktion die das
                                                                                #ganze besser macht.
            w.switchH = not w.switchH
        if w.switchH == True:
            print("FLIEß IST ABGELEGT \n p oder f drücken um Fließ zu entfernen!")   
        """    
        oldslice = slicer
        slicer += int(endtime-starttime)
        #slicer = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(slicer))
        
    documentation.append((slicer, eingegeben))    
    starttime = time.time()
    u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice)
    set_a_max()
    set_a_min()
    u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
    set_wenn_plus()
    u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
    set_clock()
    set_T_max()
    set_wenn_minus()
    plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
    if plus < 0:
        plus = 0
    print(plus)
    #write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)    
        
    return q, plus, starttime
#root.mainloop()            
#write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])

def end_process():
    global documentation, stepsprorechnung
    global slicer
    np.savetxt("documentation.csv", documentation)
    write.save(u_ges[:stepsprorechnung+slicer], alpha_ges[:stepsprorechnung+slicer], dadt_ges[:stepsprorechnung+slicer])
    print(documentation)