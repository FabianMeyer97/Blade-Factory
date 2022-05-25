import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pylab
import time

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