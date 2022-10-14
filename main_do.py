"""
Main Datei

"""
import numpy as np
#import wärmeleitung as w
import write
import reg
import time
import Einlesen as e
#import tkinter as tk
import datetime
import os

global slicer, oldslice
global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus

#experimental:
from write import testPlot, savePlot
global matplotax
global matplotcanvas
global matplotfigure
###
    

h = 0.034 #[m] # vorversuch 13; IWES Versuch 34
dy = 0.001#[m]
dt = 1
ny = int(h/dy)
dy2 = dy*dy
#Hier boundaries eingeben [in mm]:
boundary1 = None #int(7)
boundary2 = None #int((6.5+31.5))
nsteps1 = Sekunden =  int(10*60*60) # 10 hours
stepsprorechnung = int(1200) # 1200 sec = 20 min
nsteps = int(Sekunden/dt) # maximal duration for experiment ; 10 hours should be enough
alpha_start=0.01 # degree of hardening at beginning of simulation
phi=0.55                 # fiber volume content for gf laminates

maxerlaubteTemperatur = 80+273.15 #40 +273.15

plus = 20

documentation = []
np.array(documentation)  # nonsense, if you want to make an np.array, then: documentation=np.array(documentation)

plotlines=None

starttime_prefix = None
layer_composition = None

#k_core = None  #0.06 #0.06-0.0935
#density_core = None  #140
#c_core = None  #2720  

# def update_clock():
#     # get current time as text
#     current_time = datetime.datetime.now().strftime("Time: %H:%M:%S")
     
#def set_matplotcanvas(x):
#    global matplotcanvas
#    matplotcanvas = x
#def set_matplotfigure(x):
#    global matplotfigure
#    matplotfigure = x
    

def set_hswitch(switch):
    #print("regswitch is "+str(reg.switchH)+" and will be set to "+str(switch))
    reg.switchH = switch
    
def get_hswitch():
    return reg.switchH
  
def set_T_out(T):
    reg.T_out = float(T)
    
def get_T_out():
    return reg.T_out  
  
def set_u_init(T):
    reg.set_u_init(T)
    #reg.u_init = T ################
    
def get_u_init():
    return reg.get_u_init()  #################
    
def set_layer_composition(core):
    reg.set_layer_composition(core) ############
    
def set_h_luft(T):
    reg.h_luft_covered = float(T)
    
def set_alpha_start(alpha):
    global alpha_start
    #reg.alpha_start = float(alpha)
    alpha_start = float(alpha)
    
def set_fvc(x):
    #reg.fvc = float(x)
    fvc = float(x)
    
#def get_layer_composition():
#    return reg.get_layer_composition()  #################
    
def set_clock():
    global str_clock
    str_clock = "Time since start: " + str(slicer) + " sec"
    
def get_clock():
    global str_clock
    return str_clock

def set_T_max():
    global u_ges
    global str_T_max
    str_T_max = np.amax(u_ges[slicer:])-273.15
    

def get_minus():
    return np.amax(u_ges_MINUS[slicer:])-273.15       

def get_plus():
    return np.amax(u_ges_PLUS[slicer:])-273.15
#
#def set_plus(plus):
#    global plus
#    plus = plus

def get_T_max():
    global str_T_max
    return str_T_max

def set_a_max():
    global alpha_ges
    global str_a_max
    str_a_max = np.amax(alpha_ges[slicer])

def get_a_max():
    global str_a_max
    return str_a_max

#def set_max_alpha():
#    max_alpha_in_that_step = np.amax(alpha_ges[slicer:stepsprorechnung+slicer])

def get_max_alpha():
    max_alpha_in_that_step = np.amax(alpha_ges[slicer:stepsprorechnung+slicer])
    return max_alpha_in_that_step

def find_when_alpha_min():
    
    alpha_reached = 1
    alpha_reached_at = 1
    found_alpha = False
    for k in range(stepsprorechnung):
        if np.amin(alpha_ges[slicer+k,:]) >= 0.005:
            alpha_reached = np.amin(alpha_ges[slicer+k,:])
            alpha_reached_at = slicer+k
            found_alpha = True #not found_alpha
            break
    return alpha_reached, alpha_reached_at, found_alpha

def set_a_min():
    global alpha_ges
    global str_a_min
    str_a_min = np.amin(alpha_ges[slicer])

def get_a_min():
    global str_a_min
    return str_a_min


def get_alpha_min_PLUS():
    global alpha_ges_PLUS, slicer
    return np.amin(alpha_ges_PLUS[slicer])

def get_alpha_min_MINUS():
    global alpha_ges_MINUS, slicer
    return np.amin(alpha_ges_MINUS[slicer])

def get_alpha_max_PLUS():
    global alpha_ges_PLUS, slicer
    return np.amax(alpha_ges_PLUS[slicer])

def get_alpha_max_MINUS():
    global alpha_ges_MINUS, slicer
    return np.amax(alpha_ges_MINUS[slicer])

def set_wenn_plus():
    global plus, u_ges_PLUS, slicer
    global str_wenn_plus
    result = np.where(u_ges_PLUS == np.amax(u_ges_PLUS[slicer:]))
    if len(result[0]!=1) or len(result[1]!=1):
        str_wenn_plus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."
    else:
        #####str_wenn_plus = "after " + str(result[0][0]) + " sec, at " + str(result[1][0]) + " mm."
        str_wenn_plus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."

def get_wenn_plus():
    global str_wenn_plus
    return str_wenn_plus

def set_wenn_minus():
    global plus, u_ges_MINUS, slicer
    global str_wenn_minus
    result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[slicer:]))
    if len(result[0]!=1) or len(result[1]!=1):
        str_wenn_minus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."
    else:
        str_wenn_minus = "after " + str(result[0][0]) + " sec, at " + str(result[1][0]) + " mm."

def get_wenn_minus():
    global str_wenn_minus
    return str_wenn_minus

def get_delta_plus():
    return plus

def do_once(eingegeben):
    global u_ges, alpha_ges, dadt_ges, u, u0
    global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
    global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
    global plus#, slicer, oldslice, q
    global nsteps, dy, dt, dy2, ny, boundary1, boundary2, stepsprorechnung #, eingegeben1
    global documentation
    global slicer, oldslice
    global plotlines
    global starttime_prefix, layer_composition
    global alpha_start, phi
    #eingegeben1 = e.getTemperature(10)   
    documentation.append((0,eingegeben)) #documentation.append((0,eingegeben1))
    start = time.time()
    #u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung1(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben, stepsprorechnung, prefix=f"{starttime_prefix}_", layers=layer_composition) #eingegeben1
    #u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung1_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben, stepsprorechnung, plus, prefix=f"{starttime_prefix}_", layers=layer_composition) #eingegeben1
    #u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung1_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben, stepsprorechnung, plus, prefix=f"{starttime_prefix}_", layers=layer_composition) #eingegeben1
    u_ges, alpha_ges, dadt_ges, u, u0 = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, None, eingegeben, None, stepsprorechnung, None, prefix=f"{starttime_prefix}_", layers=layer_composition, first=True, alpha_start=alpha_start, phi=phi) #eingegeben1
    u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, None, eingegeben, None, stepsprorechnung, None, plus=plus, prefix=f"{starttime_prefix}_", layers=layer_composition, first=True, alpha_start=alpha_start, phi=phi) #eingegeben1
    u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, None, eingegeben, None, stepsprorechnung, None, plus=-plus, prefix=f"{starttime_prefix}_", layers=layer_composition, first=True, alpha_start=alpha_start, phi=phi) #eingegeben1
                                                      
    plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
    if plus < 0:
        plus = 0
    print(plus) #Temperaturzuschlag/abzug für Parallelrechnungen
    #write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)   
    global matplotcanvas, matplotax
    plotlines = testPlot(matplotfigure, matplotax,u_ges[:stepsprorechnung], stepsprorechnung, 0)
    print(plotlines)
    slicer = 0
    oldslice = 0
    q = -1
    return q, start, plus
    
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def do_process(q, start, starttime, eingegeben): #, plus ???????????? ist das plus nicht notwendig für mainWindowTK??????????
    #clearConsole()
    global u_ges, alpha_ges, dadt_ges, u, u0
    global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
    global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
    global plus#, slicer, oldslice, q
    global nsteps, dy, dt, dy2, ny, boundary1, boundary2, stepsprorechnung #, eingegeben1
    global documentation
    global slicer, oldslice
    global matplotcanvas, matplotax
    global plotlines, matplotfigure
    global starttime_prefix, layer_composition
    global alpha_start, phi
    q += 1  
    
    
    endtime = time.time()
    #matplotax.clear()
    if q == 0:   
        dif1 = int(endtime-start)
        #dif1 = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(dif1))
        slicer += dif1 # # slicer was 0 and is noch dif1?
    else: 
        #Die entfernten Zeilen müssen in der TKinter Datei angepasst werden --> "Schalter"Funktion die durch button klick ausgelöst wird
        oldslice = slicer
        slicer += int(endtime-starttime)
        #slicer = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(slicer))
        
    documentation.append((slicer, eingegeben))    
    starttime = time.time()
    plus = (maxerlaubteTemperatur - np.amax(u_ges))/2 
    if plus < 1: #0: # lower steps than 1 degree probably not useful
        plus = 1 # 0
    
    #print(plus)
    
    u_ges, alpha_ges, dadt_ges, u, u0 = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice, 
                                                        write=False, prefix=f"{starttime_prefix}_", layers=layer_composition, 
                                                        u_ges=u_ges[:stepsprorechnung+oldslice], 
                                                        alpha_ges=alpha_ges[:stepsprorechnung+oldslice], 
                                                        dadt_ges=dadt_ges[:stepsprorechnung+oldslice],                                      
                                                        first=False, silent=False, alpha_start=alpha_start, phi=phi)
    set_a_max()
    set_a_min()
    #set_max_alpha()
    u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS,u0_PLUS = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, 
                                                                                plus=plus, write=False, prefix=f"{starttime_prefix}_", layers=layer_composition, 
                                                                                u_ges=u_ges_PLUS[:stepsprorechnung+oldslice], 
                                                                                alpha_ges=alpha_ges_PLUS[:stepsprorechnung+oldslice], 
                                                                                dadt_ges=dadt_ges_PLUS[:stepsprorechnung+oldslice],                                      
                                                                                first=False, silent=True, alpha_start=alpha_start, phi=phi)
    set_wenn_plus()
    u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, 
                                                                                plus=-plus, write=False, prefix=f"{starttime_prefix}_", layers=layer_composition,
                                                                                u_ges=u_ges_MINUS[:stepsprorechnung+oldslice], 
                                                                                alpha_ges=alpha_ges_MINUS[:stepsprorechnung+oldslice], 
                                                                                dadt_ges=dadt_ges_MINUS[:stepsprorechnung+oldslice],                                      
                                                                                first=False, silent=True, alpha_start=alpha_start, phi=phi)
    set_clock()
    set_T_max()
    set_wenn_minus()
    #result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[slicer:]))
    # str_wenn_minus = "wenn - "+str(int(plus))+ "°C: " + str(np.amax(u_ges_MINUS[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm."
    # bsser am anfang?
    #plus = (maxerlaubteTemperatur - np.amax(u_ges))/2 # wird erst beim nächsten update für regelung2 verwendet
    #if plus < 0:
    #    plus = 0
    #print(plus)
    #write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)    
    #time.sleep(0.1)
    testPlot(matplotfigure, matplotax,u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer, slicer, update=plotlines)
    #savePlot("regelung-plot.svg") # does not show up if not saved...
        
    return q, plus, starttime           
#write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])

def end_process():
    global documentation, stepsprorechnung
    global slicer, q
    global starttime_prefix, layer_composition
    np.savetxt(f"{starttime_prefix}_documentation.csv", documentation)
    write.save(u_ges[:stepsprorechnung+slicer], alpha_ges[:stepsprorechnung+slicer], dadt_ges[:stepsprorechnung+slicer], prefix=f"{starttime_prefix}_")
    #write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer) 
    global matplotcanvas, matplotax
    testPlot(matplotax, matplotax,u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer, slicer)
    savePlot(f"{starttime_prefix}_regelung-plot.svg")
    print(documentation)