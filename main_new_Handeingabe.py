"""
Main Datei

"""
import numpy as np
import wärmeleitung as w
import write
import reg
import time
#import Einlesen as e

h = 0.013 #[m]
dy = 0.001#[m]
dt = 1
ny = int(h/dy)
dy2 = dy*dy
#Hier boundaries eingeben [in mm]:
boundary1 = int(7)
boundary2 = int((6.5+31.5))
nsteps1 = Sekunden =  int(5*60*60)
stepsprorechnung = int(1200)
nsteps = int(Sekunden/dt)

p1 = int(17*60/dt)
p2 = int(50*60/dt)
p3 = int(110*60/dt)
p4 = int(350*60/dt)

#widerholungen = 2000
#u00 = write.readu0()
#u00 = np.genfromtxt("S1.csv")
#print(u00.size)

#nsteps = int(u00.size/dt)

#u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges = calculations.calcIt_real(p1,p2,p3,p4,nsteps, dy, dt, dy2, ny, boundary1, boundary2)
#u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges = calculations.calcIt_S1(p1,p2,p3,p4,nsteps, dy, dt, dy2, ny, boundary1, boundary2)

plus = 20

documentation = []
np.array(documentation)

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
    
documentation.append((0,eingegeben1))
start = time.time()
u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung1(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung)
u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung1_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung1_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingegeben1, stepsprorechnung, plus)
plus = (np.amax(u_ges) - eingegeben1)/2
print(plus)

write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)


slicer = 0
oldslice = 0
q = -1
while True:  
    q += 1  
    if q == 0:
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
        plus = (np.amax(u_ges) - eingegeben)/2
        write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)
        
    else: 
        
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
              
        endtime = time.time()
        oldslice = slicer
        slicer += int(endtime-starttime)
        slicer = int(input("Slicer"))
        print("Verstrichende Zeit in Sekunden: " + str(slicer))
        documentation.append((slicer, eingegeben))
        starttime = time.time()
        u_ges, alpha_ges, dadt_ges, u, u0 = reg.regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben, slicer, stepsprorechnung, oldslice)
        u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS = reg.regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
        u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS = reg.regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus)
        plus = (np.amax(u_ges) - eingegeben)/2
        write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)    
            
#write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])
np.savetxt("documentation.csv", documentation)
write.save(u_ges[:stepsprorechnung+slicer], alpha_ges[:stepsprorechnung+slicer], dadt_ges[:stepsprorechnung+slicer])
print(documentation)
#u0, u, u_ges = w.kelvin_to_celsius(u0, u, u_ges)

#u_ges[-1,:] += 273.15

"""
test = np.zeros(ny)
for b in range(5):
    q = b*1000
    test = np.vstack((test[::2], u_ges[q,::2]))

np.savetxt("Verlgeich2 dt = " + str(dt) + "dy = " + str(dy) + ".txt", test, fmt = "%.2f")
"""
#write.showH(u_ges, h_luft_ges, nsteps1, dt)
#write.colormap(u_ges, dadt_ges)
#write.plot_heatmap2(nsteps, dt, u_ges, h, dy, ny) 
#write.vergleich_plot_heatmap(nsteps, dt, u_ges, h, dy, ny)
#write.heatVergleichS1(nsteps, u_ges)
#write.heatVergleich(nsteps, u_ges)
#write.heatVergleichfirst5000(nsteps, u_ges)
#write.heatVergleichfirst3000to20000(nsteps, u_ges)

"""
for k in range(int(ny)):
    write.writeToTxt(int(k), nsteps, reak_kinetic_ges, dadt_ges, u_ges, alpha_ges, dt, dy, ny, boundary1, boundary2)
write.writeToTxt1(0, nsteps, reak_kinetic_ges, dadt_ges, u_ges, alpha_ges, dt, dy, ny, boundary1, boundary2)
"""