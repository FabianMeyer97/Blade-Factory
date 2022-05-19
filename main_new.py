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

def update_clock():
    # get current time as text
    current_time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    
    lab.config(text=current_time)
    #lab['text'] = current_time 
    root.after(1000, update_clock) 

# --- main ---
root = tk.Tk()
lab = tk.Label(root)
lab.pack()
update_clock()


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

write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)


slicer = 0
oldslice = 0
q = -1
while True:  
    q += 1  
    if q == 0:
        """
        while True:
            try:     
                eingegeben = int(input("Aktuelle Heizplattentemp in °C: "))+273.15
                #eingegeben1 = e.getTemperature(10)
            except ValueError:
                print("Keine Integer-Zahl eingegeben")
            else:
                if (eingegeben > 0+273.15 and eingegeben < 150+273.15):
                    break   
                print("Wert zu hoch oder zu gering!")
        """
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
        """
        while True:
            try:     
                eingegeben = int(input("Aktuelle Heizplattentemp in °C: "))+273.15
                #eingegeben1 = e.getTemperature(10)
            except ValueError:
                print("Keine Integer-Zahl eingegeben")
            else:
                if eingegeben == 999+273.15 or eingegeben == 555+273.15 or (eingegeben > 0+273.15 and eingegeben < 150+273.15):
                    break   
                print("Wert zu hoch oder zu gering!")
                
        if eingegeben == 999+273.15:
            break
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
        eingegeben = e.getTemperature(10)      
        endtime = time.time()
        oldslice = slicer
        slicer += int(endtime-starttime)
        #slicer = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(slicer))
        documentation.append((slicer, eingegeben))
        starttime = time.time()
        u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice)
        u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
        u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
        plus = (maxerlaubteTemperatur - np.amax(u_ges))/2
        if plus < 0:
            plus = 0
        print(plus)
        write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)    
root.mainloop()            
#write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])
np.savetxt("documentation.csv", documentation)
write.save(u_ges[:stepsprorechnung+slicer], alpha_ges[:stepsprorechnung+slicer], dadt_ges[:stepsprorechnung+slicer])
print(documentation)