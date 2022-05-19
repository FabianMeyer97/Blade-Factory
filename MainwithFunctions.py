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
import tkinter as tk
import datetime
import threading


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

maxerlaubteTemperatur = 41 +273.15

firstplus = 20

documentation = ["Gestartet um: " + str(datetime.datetime.now().strftime(" %H:%M:%S"))]
np.array(documentation)

def firstIteration(firstplus):
    plus = firstplus
    eingegeben1 = e.getTemperature(10)   
    documentation.append((0,eingegeben1))
    start = time.time()
    u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung1(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung)
    u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung1_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
    u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung1_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
    plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
    if plus < 0:
        plus = 0
    write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)
    
    return start, plus


start, plus = firstIteration(firstplus)

slicer = 0
oldslice = 0
q = -1
cool1 = True
def followingIterations(slicer, oldslice, q, start, plus):
    
    while cool1:
        
        q += 1  
        if q == 0:

            eingegeben = e.getTemperature(10)
            end = time.time()
            dif1 = int(end-start)
            #dif1 = int(input("Slicer"))
            print("Verstrichende Zeit in Sekunden: " + str(dif1))
            documentation.append((dif1, eingegeben))
            slicer += dif1 
            starttime = time.time()
            u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice)
            u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
            u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
            plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
            if plus < 0:
                plus = 0
    
            write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)
            
        else:   
            eingegeben = e.getTemperature(10)      
            endtime = time.time()
            oldslice = slicer
            slicer += int(endtime-starttime)
            #slicer = int(input("Slicer"))
            print("Verstrichende Zeit in Sekunden: " + str(slicer))
            documentation.append((slicer, eingegeben))
            starttime = time.time()
            u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice)
            if plus != 0:    
                u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
                u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
            else:
                print("PLUS/MINUS nicht durchgeführt da 0 \n \n")
            plus = int((maxerlaubteTemperatur - np.amax(u_ges))/2)
            if plus < 0:
                plus = 0
            write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)
            time.sleep(5)
            #lab.config(text=slicer)
            #lab['text'] = slicer
            #root.after(1000, followingIterations)                

    return u_ges, alpha_ges, dadt_ges, documentation

def starty():       
    followingIterations(slicer, oldslice, q, start, plus)
    return

def coolwow():
    w.switchH = not w.switchH
    return w.switchH
def startFollowingCalcs(): #function doing intense computation
    followingIterations(slicer, oldslice, q, start, plus)    

def get_input():
    while True:
        if keyboard.read_key() == "p":
            w.switchH = True
            print("Fließ abgelegt")
        if keyboard.read_key() == "q":
            w.switchH = False
            print("Fließ weggenommen")         
            
input_thread = threading.Thread(target=get_input)
input_thread.start()

startFollowingCalcs()

#write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])
np.savetxt("documentation.csv", documentation)
#write.save(u_ges[:stepsprorechnung+slicer], alpha_ges[:stepsprorechnung+slicer], dadt_ges[:stepsprorechnung+slicer])
print(documentation)