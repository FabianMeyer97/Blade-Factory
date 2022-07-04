# -*- coding: utf-8 -*-
"""
mainConsole
"""

import main_do
import threading as th
import numpy as np

global u_ges, alpha_ges, dadt_ges, u, u0
global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
#global plus#, slicer, oldslice, q
global nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung
global documentation
    
global q, start, slicer, oldslice, plus

#experimentell:
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
matplotlib.rcParams['interactive'] = False
###

def promptTemperature():
    while True:
        try:     
            eingegeben = int(input("Aktuelle Heizplattentemp in °C: "))+273.15
            #eingegeben1 = e.getTemperature(10)
        except ValueError:
            print("Keine Integer-Zahl eingegeben")
        else:
            if eingegeben == 999+273.15 or eingegeben == 555+273.15  or eingegeben == 888+273.15 or (eingegeben > 0+273.15 and eingegeben < 150+273.15):
                break   
            print("Wert zu hoch oder zu gering!")
    return eingegeben

eingegeben = promptTemperature()

global starttime

# initialize plot axis
figure, main_do.matplotax = plt.subplots()

#global q, start, slicer, oldslice, plus
q, start, plus = main_do.do_once(eingegeben)
starttime = None

    

while True:  
    eingegeben = promptTemperature()
            
    if eingegeben == 999+273.15:
        break
    if eingegeben == 555+273.15:            
         w.switchH = not w.switchH
         continue
         
    if eingegeben == 888+273.15:        
        plt.show()
        continue
    """
    if keyboard.read_key() == "p" or keyboard.read_key() == "f":            #Hier wird auf Eingabe gewartet tkinter hat wohl eine Funktion die das
                                                                            #ganze besser macht.
        w.switchH = not w.switchH
    if w.switchH == True:
        print("FLIEß IST ABGELEGT \n p oder f drücken um Fließ zu entfernen!")   
    """    
    q, plus, starttime = main_do.do_process(q, start, plus, starttime, eingegeben) # main_do.do_process(q, start, slicer, oldslice, plus, starttime) #, slicer, oldslice, 
    
    
main_do.end_process() 