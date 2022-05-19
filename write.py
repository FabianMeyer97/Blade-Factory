import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pylab
import time

def plot_heatmap(nsteps, dt, u_ges, h, dy, ny):
    
    yarray = np.linspace(0,h-dy, ny)
                         
    plt.clf()
    #Temperaturverteilung bei letztem Zeitinkrement
    plt.title("Temperaturverlauf")
    plt.xlabel("Weg in mm")
    plt.ylabel("Temperatur in °C")
    plt.grid(True, linestyle=':', alpha = 0.5)
    plt.plot(yarray, u_ges[-2,:], label = "base temp")
    
    return plt

def plot_heatmap1(nsteps, dt, u_ges, h, dy, ny):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

                         
    plt.clf()
    #Temperaturverteilung bei letztem Zeitinkrement
    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")
    
    plt.grid(True, linestyle=':', alpha = 0.5)
    
    for m in range(3):
        plt.plot(narray, u_ges[:,int((m*4)/(1000*dy))], label = int((m*4)/(1000*dy)))
        
    plt.plot(narray, u_ges[:,int((12)/(1000*dy))], label = int((43)/(1000*dy)))  
             
    plt.legend()
    
    return plt

def plot_heatmap2(nsteps, dt, u_ges):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

                         
    plt.clf()
    #Temperaturverteilung bei letztem Zeitinkrement
    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")
    
    plt.grid(True, linestyle=':', alpha = 0.5)
    plt.plot(narray, u_ges[:,0]-273.15, label = int(0))
    plt.plot(narray, u_ges[:,3]-273.15, label = int(3))
    plt.plot(narray, u_ges[:,8]-273.15, label = int(8))
    plt.plot(narray, u_ges[:,12]-273.15, label = int(12))

    plt.legend()
    
    return plt

def vergleich_plot_heatmap(nsteps, dt, u_ges, h, dy, ny):
    
    yarray = np.linspace(0,h-dy, ny)
    
    for b in range(5): 
                    
        plt.clf()
        #Temperaturverteilung bei letztem Zeitinkrement
        plt.title("1Temperaturverlauf nach " + str((b/60)*100000) + " mins " + str(dy) + " dy")
        plt.xlabel("Weg in mm")
        plt.ylabel("Temperatur in °C")
        plt.grid(True, linestyle=':', alpha = 0.5)
        plt.plot(yarray, u_ges[b*1000,:])
        plt.savefig("1.0Temperaturverlauf nach " + str((b/60)*100000) + " mins dy =" + str(dy) +".png")
    return plt


#Colormap die gesamten Array farblich darstellt über Zeit und Weg
def colormap(u_ges, dadt):
    plt.clf()
    #Temperaturverteilung bei letztem Zeitinkrement
    plt.title("Temperaturverlauf über Zeit")
        
    plt.xlabel("weg in mm")
    plt.ylabel("Steps in 1/dt")

    plt.pcolormesh(u_ges, cmap=plt.cm.jet, vmin=np.amin(u_ges), 
                       vmax=np.amax(u_ges))
    plt.colorbar()
    #plt.savefig("Colormap")
    plt.show()
    
    return plt

def heatVergleichS1(nsteps, u_ges):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h
        
    
    S1 = np.genfromtxt("S1.csv")
    S3 = np.genfromtxt("S3.txt")
    S5 = np.genfromtxt("S5.txt")
    S6 = np.genfromtxt("S6.txt")
    S8 = np.genfromtxt("S8.txt")
    S10 = np.genfromtxt("S10.txt")
    
    plt.clf()

    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")

    plt.grid(True, linestyle=':', alpha = 0.5)

    plt.plot(narray, u_ges[:,0], label = int(0), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,4], label = int(4), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,6], label = int(6), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,39], label = int(39), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,43], label = int(43), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,45], label = int(45), color = "red", alpha = 0.5)

    
    plt.plot(narray, S1, label = "S1", color = "blue", alpha = 0.5)
    #plt.plot(narray, S3, label = "S3", color = "blue", alpha = 0.5)
    plt.plot(narray, S5, label = "S5", color = "blue", alpha = 0.5)
    plt.plot(narray, S6, label = "S6", color = "blue", alpha = 0.5)
    plt.plot(narray, S8, label = "S8", color = "blue", alpha = 0.5)    
    plt.plot(narray, S10, label = "S10", color = "blue", alpha = 0.5)
    
    plt.legend()

def heatVergleich(nsteps, u_ges):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h
        
   
    L1 = np.genfromtxt("INPUT.csv")
    L2 = np.genfromtxt("L2.csv")
    L3 = np.genfromtxt("L3.csv")
    L4 = np.genfromtxt("L4.csv")
    
    plt.clf()

    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")

    plt.grid(True, linestyle=':', alpha = 0.5)

    plt.plot(narray, u_ges[:,0], label = int(0), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,3], label = int(3), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,8], label = int(8), color = "red", alpha = 0.5)
    plt.plot(narray, u_ges[:,12], label = int(12), color = "red", alpha = 0.5)
   
    plt.plot(narray, L1, label = "L1", color = "blue", alpha = 0.5)
    plt.plot(narray, L2, label = "L2", color = "blue", alpha = 0.5)
    plt.plot(narray, L3, label = "L3", color = "blue", alpha = 0.5)
    plt.plot(narray, L4, label = "L4", color = "blue", alpha = 0.5)
      
    plt.legend()

def heatVergleichfirst5000(nsteps, u_ges):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

    L1 = np.genfromtxt("INPUT.csv")
    L2 = np.genfromtxt("L2.csv")
    L3 = np.genfromtxt("L3.csv")
    L4 = np.genfromtxt("L4.csv")

    plt.clf()

    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")

    plt.grid(True, linestyle=':', alpha = 0.5)

    plt.plot(narray[:5000], u_ges[:5000,0], label = int(0), color = "red", alpha = 0.5)
    plt.plot(narray[:5000], u_ges[:5000,3], label = int(3), color = "red", alpha = 0.5)
    plt.plot(narray[:5000], u_ges[:5000,8], label = int(8), color = "red", alpha = 0.5)
    plt.plot(narray[:5000], u_ges[:5000,12], label = int(12), color = "red", alpha = 0.5)

    plt.plot(narray[:5000], L1[:5000], label = "L1", color = "blue", alpha = 0.5)
    plt.plot(narray[:5000], L2[:5000], label = "L2", color = "blue", alpha = 0.5)
    plt.plot(narray[:5000], L3[:5000], label = "L3", color = "blue", alpha = 0.5)
    plt.plot(narray[:5000], L4[:5000], label = "L4", color = "blue", alpha = 0.5)
    
    plt.legend()    

def heatVergleichfirst3000to20000(nsteps, u_ges):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

    L1 = np.genfromtxt("INPUT.csv")
    L2 = np.genfromtxt("L2.csv")
    L3 = np.genfromtxt("L3.csv")
    L4 = np.genfromtxt("L4.csv")

    plt.clf()

    plt.title("Temperaturverlauf")
    plt.xlabel("Steps")
    plt.ylabel("Temperatur in °C")

    plt.grid(True, linestyle=':', alpha = 0.5)

    plt.plot(narray[3000:20000], u_ges[3000:20000,0], label = int(0), color = "red", alpha = 0.5)
    plt.plot(narray[3000:20000], u_ges[3000:20000,3], label = int(3), color = "red", alpha = 0.5)
    plt.plot(narray[3000:20000], u_ges[3000:20000,8], label = int(8), color = "red", alpha = 0.5)
    plt.plot(narray[3000:20000], u_ges[3000:20000,12], label = int(12), color = "red", alpha = 0.5)

    plt.plot(narray[3000:20000], L1[3000:20000], label = "L1", color = "blue", alpha = 0.5)
    plt.plot(narray[3000:20000], L2[3000:20000], label = "L2", color = "blue", alpha = 0.5)
    plt.plot(narray[3000:20000], L3[3000:20000], label = "L3", color = "blue", alpha = 0.5)
    plt.plot(narray[3000:20000], L4[3000:20000], label = "L4", color = "blue", alpha = 0.5)
    
    plt.legend()    

def writeToTxt(j, nsteps, reak_kinetik_ges, dadt_ges, u_ges, alpha_ges, dt, dy, ny, boundary1, boundary2):
   
    time = np.linspace(0, nsteps-1, nsteps)
    reak_multiplier = np.ones(ny)
    reak_multiplier[boundary1:boundary2] = 0    
    w_ges = reak_kinetik_ges# * reak_multiplier
            
    secs = np.zeros((nsteps, ny))

    for q in range(nsteps):
        secs[q,:] = time[q] * dt
    
    #ges = np.stack((secs, u_ges, alpha_ges, dadt_ges, w_ges), axis = -1)
    ges = np.stack((u_ges, alpha_ges, dadt_ges, w_ges), axis = -1) 
    ges_2 = ges[::60]
    np.savetxt("dt = " + str(dt) + ", dy = " + str(dy*1000) + " at " + str (j*0.001*1000) + "mm.txt",
               ges_2[:,j], fmt = "%.2f\t" + "%.3e\t" *2 + "%.3e")
    return

def writeToTxt1(j, nsteps, reak_kinetik_ges, dadt_ges, u_ges, alpha_ges, dt, dy, ny, boundary1, boundary2):
   
    time = np.linspace(0, nsteps-1, nsteps)
    reak_multiplier = np.ones(ny)
    reak_multiplier[boundary1:boundary2] = 0    
    w_ges = reak_kinetik_ges# * reak_multiplier
            
    secs = np.zeros((nsteps, ny))

    for q in range(nsteps):
        secs[q,:] = time[q] * dt
    
    #ges = np.stack((secs, u_ges, alpha_ges, dadt_ges, w_ges), axis = -1)
    ges = np.stack((secs, u_ges, alpha_ges, dadt_ges, w_ges), axis = -1) 
    ges_2 = ges[::60]
    np.savetxt("dt = " + str(dt) + ", dy = " + str(dy*1000) + " at " + str (j*0.001*1000) + "mm.txt",
               ges_2[:,j], fmt = "%.2f\t"*2 + "%.3e\t" *2 + "%.3e")
    return

def showH(u_ges, h_luft_ges, nsteps1, dt):
    
    t = np.arange(0, nsteps1, dt)
    fig, ax1 = plt.subplots()
    color = "red"
    ax1.set_xlabel("zeit in sek")
    ax1.set_ylabel("Temperatur in °C", color = color)
    ax1.plot(t, u_ges[:,-1], color=color)
    ax1.tick_params(axis = "y", labelcolor = color)
    
    ax2 = ax1.twinx()
    
    color = "blue"
    ax2.set_ylabel("h", color = color)
    ax2.plot(t, h_luft_ges[:,-1], color = color)
    ax2.tick_params(axis = "y", labelcolor = color)
    
    fig.tight_layout()
    plt.show()
    
    return

def save(u_ges_write, alpha_ges_write, dadt_ges_write):
    
    np.savetxt("u_ges.csv", u_ges_write, delimiter = ",")
    np.savetxt("alpha_ges.csv", alpha_ges_write, delimiter = ",")
    np.savetxt("dadt_ges.csv", dadt_ges_write, delimiter = ",")
    
def save_PLUS(u_ges_PLUS_write, alpha_ges_PLUS_write, dadt_ges_PLUS_write):
    
    np.savetxt("u_ges_PLUS.csv", u_ges_PLUS_write, delimiter = ",")
    np.savetxt("alpha_ges_PLUS.csv", alpha_ges_PLUS_write, delimiter = ",")
    np.savetxt("dadt_ges_PLUS.csv", dadt_ges_PLUS_write, delimiter = ",")
 
def save_MINUS(u_ges_MINUS_write, alpha_ges_MINUS_write, dadt_ges_MINUS_write):
    
    np.savetxt("u_ges_MINUS.csv", u_ges_MINUS_write, delimiter = ",")
    np.savetxt("alpha_ges_MINUS.csv", alpha_ges_MINUS_write, delimiter = ",")
    np.savetxt("dadt_ges_MINUS.csv", dadt_ges_MINUS_write, delimiter = ",")
    
def read():
    
    u_ges_read = np.genfromtxt("u_ges.csv", delimiter = ",")
    alpha_ges_read = np.genfromtxt("alpha_ges.csv", delimiter = ",")
    dadt_ges_read = np.genfromtxt("dadt_ges.csv", delimiter = ",")
    
    return u_ges_read, alpha_ges_read, dadt_ges_read

def read_PLUS():
    
    u_ges_PLUS_read = np.genfromtxt("u_ges_PLUS.csv", delimiter = ",")
    alpha_ges_PLUS_read = np.genfromtxt("alpha_ges_PLUS.csv", delimiter = ",")
    dadt_ges_PLUS_read = np.genfromtxt("dadt_ges_PLUS.csv", delimiter = ",")
    
    return u_ges_PLUS_read, alpha_ges_PLUS_read, dadt_ges_PLUS_read

def read_MINUS():
    
    u_ges_MINUS_read = np.genfromtxt("u_ges_MINUS.csv", delimiter = ",")
    alpha_ges_MINUS_read = np.genfromtxt("alpha_ges_MINUS.csv", delimiter = ",")
    dadt_ges_MINUS_read = np.genfromtxt("dadt_ges_MINUS.csv", delimiter = ",")
    
    return u_ges_MINUS_read, alpha_ges_MINUS_read, dadt_ges_MINUS_read

def readu0():    
    return np.genfromtxt("INPUT.csv")#, delimiter = ",")

def drawplot():
    
    pylab.ion()
    
    line, = pylab.plot(0,1,"ro", markersize = 8)
    pylab.axis([0,1,0,1])
    
    line.set_xdata([1,2,3])
    line.set_ydata([1,2,3])
    pylab.draw()
    
    time.sleep(6)
    line1, = pylab.plot([4], [5], "g*", markersize=8)
    pylab.draw()
    
    for i in range(10):
        line.set_xdata([1,2,3])
        line.set_ydata([1,2,3])
        pylab.draw()
        time.sleep(1)
    line2, = pylab.plot(3,2, "b^", markersize=8)  
    pylab.draw()
    time.sleep(20)
    return

def animatePlot(u_ges, nsteps):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

    fig, ax = plt.subplots()
    
    xdata1, ydata1 = narray, u_ges[:,0]-273.15
    xdata2, ydata2 = narray, u_ges[:,3]-273.15
    xdata3, ydata3 = narray, u_ges[:,9]-273.15
    xdata4, ydata4 = narray, u_ges[:,12]-273.15
    
    ln1, = plt.plot(narray, u_ges[:,0]-273.15, label = "0")#, markersize = 1)
    ln2, = plt.plot(narray, u_ges[:,3]-273.15, label = "3")#, markersize = 1)
    ln3, = plt.plot(narray, u_ges[:,9]-273.15, label = "9")#, markersize = 1)
    ln4, = plt.plot(narray, u_ges[:,12]-273.15, label = "12")#, markersize = 1)
    

    def init():
        
        plt.title("Regelungsimulation")
        ax.set_xlabel("Zeit in Sekunden")
        ax.set_ylabel("Temperatur in °C")
        plt.legend()
        #ax.set_xlim(0, 2*np.pi)
        #ax.set_ylim(-1, 1)
        return ln1 ,ln2, ln3, ln4

    def update(frame):
        xdata1.append(frame)
        ydata1.append(np.sin(frame))
        xdata2.append(frame)
        ydata2.append(np.sin(frame))
        
        ln1.set_data(xdata1, ydata1)
        ln2.set_data(xdata2, ydata2)
        ln3.set_data(xdata3, ydata3)
        ln2.set_data(xdata4, ydata4)        
        
        return ln1, ln2, ln3, ln4

    ani = FuncAnimation(fig, update, frames=narray, repeat = False,
                        init_func=init, blit=True)
    plt.show()
    
    return ani




def animatePlot1(u_ges, u_ges_PLUS, nsteps):
    
    narray = np.ones(nsteps)
    
    for h in range(nsteps):
        narray[h] = h

    fig, ax = plt.subplots()
    
    xdata1, ydata1 = narray, u_ges[:,0]-273.15
    xdata2, ydata2 = narray, u_ges[:,3]-273.15
    xdata3, ydata3 = narray, u_ges[:,9]-273.15
    xdata4, ydata4 = narray, u_ges[:,12]-273.15
    
    ln1, = plt.plot(narray, u_ges[:,0]-273.15, 'g', label = "0")#, markersize = 1)
    ln2, = plt.plot(narray, u_ges[:,3]-273.15, 'g', label = "3")#, markersize = 1)
    ln3, = plt.plot(narray, u_ges[:,9]-273.15, 'g', label = "9")#, markersize = 1)
    ln4, = plt.plot(narray, u_ges[:,12]-273.15, 'g', label = "12")#, markersize = 1)
    
    ln5, = plt.plot(narray, u_ges_PLUS[:,0]-273.15, 'r', label = "+5: 0")#, markersize = 1)
    ln6, = plt.plot(narray, u_ges_PLUS[:,3]-273.15, 'r', label = "+5: 3")#, markersize = 1)
    ln7, = plt.plot(narray, u_ges_PLUS[:,9]-273.15, 'r', label = "+5: 9")#, markersize = 1)
    ln8, = plt.plot(narray, u_ges_PLUS[:,12]-273.15, 'r', label = "+5: 12")#, markersize = 1)
    
    def init():
        
        plt.title("Regelungsimulation")
        ax.set_xlabel("Zeit in Sekunden")
        ax.set_ylabel("Temperatur in °C")
        plt.legend()
        #ax.set_xlim(0, 2*np.pi)
        #ax.set_ylim(-1, 1)
        return ln1 ,ln2, ln3, ln4

    def update(frame):
        xdata1.append(frame)
        ydata1.append(np.sin(frame))
        xdata2.append(frame)
        ydata2.append(np.sin(frame))
        
        ln1.set_data(xdata1, ydata1)
        ln2.set_data(xdata2, ydata2)
        ln3.set_data(xdata3, ydata3)
        ln2.set_data(xdata4, ydata4)        
        
        return ln1, ln2, ln3, ln4

    ani = FuncAnimation(fig, update, frames=narray,
                        init_func=init, blit=True)
    plt.show()
    
    return ani