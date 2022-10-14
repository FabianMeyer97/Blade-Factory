"""
This file contains functions for plotting, writing and reading data
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pylab
import time

starttime_prefix = None

#Save the temperature, alpha and dadt data as .csv-files
def save(u_ges_write, alpha_ges_write, dadt_ges_write, **kwargs): 
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
    if "plus" in kwargs:
        plus="_"+str('{0:+d}'.format(round(kwargs["plus"])))
    else:
        plus=""
    np.savetxt(f"{prefix}u_ges{plus}.csv", u_ges_write, delimiter = ",")  #f"({main_do.get_a_min():.2%}, {main_do.get_a_max():.2%})"
    np.savetxt(f"{prefix}alpha_ges{plus}.csv", alpha_ges_write, delimiter = ",")
    np.savetxt(f"{prefix}dadt_ges{plus}.csv", dadt_ges_write, delimiter = ",")
    
def save_PLUS(u_ges_PLUS_write, alpha_ges_PLUS_write, dadt_ges_PLUS_write, **kwargs):
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
        
    np.savetxt(f"{prefix}u_ges_PLUS.csv", u_ges_PLUS_write, delimiter = ",")
    np.savetxt(f"{prefix}alpha_ges_PLUS.csv", alpha_ges_PLUS_write, delimiter = ",")
    np.savetxt(f"{prefix}dadt_ges_PLUS.csv", dadt_ges_PLUS_write, delimiter = ",")
 
def save_MINUS(u_ges_MINUS_write, alpha_ges_MINUS_write, dadt_ges_MINUS_write, **kwargs):
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
    np.savetxt(f"{prefix}u_ges_MINUS.csv", u_ges_MINUS_write, delimiter = ",")
    np.savetxt(f"{prefix}alpha_ges_MINUS.csv", alpha_ges_MINUS_write, delimiter = ",")
    np.savetxt(f"{prefix}dadt_ges_MINUS.csv", dadt_ges_MINUS_write, delimiter = ",")
    
#Read temperature, alpha and dadt data from .csv-files    
def read(**kwargs):
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
    u_ges_read = np.genfromtxt(f"{prefix}u_ges.csv", delimiter = ",")
    alpha_ges_read = np.genfromtxt(f"{prefix}alpha_ges.csv", delimiter = ",")
    dadt_ges_read = np.genfromtxt(f"{prefix}dadt_ges.csv", delimiter = ",")
    return u_ges_read, alpha_ges_read, dadt_ges_read

def read_PLUS(**kwargs):
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
    u_ges_PLUS_read = np.genfromtxt(f"{prefix}u_ges_PLUS.csv", delimiter = ",")
    alpha_ges_PLUS_read = np.genfromtxt(f"{prefix}alpha_ges_PLUS.csv", delimiter = ",")
    dadt_ges_PLUS_read = np.genfromtxt(f"{prefix}dadt_ges_PLUS.csv", delimiter = ",")
    return u_ges_PLUS_read, alpha_ges_PLUS_read, dadt_ges_PLUS_read

def read_MINUS(**kwargs):
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
    u_ges_MINUS_read = np.genfromtxt(f"{prefix}u_ges_MINUS.csv", delimiter = ",")
    alpha_ges_MINUS_read = np.genfromtxt(f"{prefix}alpha_ges_MINUS.csv", delimiter = ",")
    dadt_ges_MINUS_read = np.genfromtxt(f"{prefix}dadt_ges_MINUS.csv", delimiter = ",")
    return u_ges_MINUS_read, alpha_ges_MINUS_read, dadt_ges_MINUS_read

#Plotfunctions:
def drawplot():
    
    #pylab.ion()
    
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

def testPlot(canvas,ax,u_ges, nsteps, q, **kwargs):  #def testPlot(self,canvas,ax):
    #c = ['r','b','g']  # plot marker colors
    narray = np.array([i for i in range(nsteps)])
    
    if "update" in kwargs:
        lns=kwargs["update"]

        lns[0].set_xdata(narray[:q])
        lns[1].set_xdata(narray)
        lns[2].set_xdata(narray)
        lns[3].set_xdata(narray)
        lns[4].set_xdata(q)
        lns[4].set_label(f"{q} sec since start")
        #fm = plt.get_current_fig_manager()
        #fm.toolbar.actions()[0].triggered.connect(home_callback)
        ax.legend()
        
        lns[0].set_ydata(u_ges[:q,0]-273.15)
        lns[1].set_ydata(u_ges[:,1]-273.15)
        lns[2].set_ydata(u_ges[:,6]-273.15)
        lns[3].set_ydata(u_ges[:,7]-273.15)
        
        
        #redraw plot
        ax = plt.gca()
        ax.relim()
        ax.autoscale_view()
         
        figure = plt.gcf()
        #figure.canvas.draw_idle() 
        figure.canvas.draw()
        #figure.canvas.flush_events()
        #plt.pause(0.05)
        return lns
    else:
        ax.clear()   
            
        #fig, ax = plt.subplots()
        plt.title("Regelungsimulation")
        #ax.set_xlabel("Zeit in Sekunden")
        #ax.set_ylabel("Temperatur in °C")
        plt.xlabel("time",fontsize=18)
        plt.ylabel("$T$ in °C",fontsize=18)    
        
        ln1, = plt.plot(narray[:q], u_ges[:q,0]-273.15, label = "0 mm")#, markersize = 1)
        ln2, = plt.plot(narray, u_ges[:,1]-273.15, label = "4 mm")#, markersize = 1)
        #ln5, = plt.plot(narray, u_ges[:,6]-273.15, label = "6")#, markersize = 1)
        ln3, = plt.plot(narray, u_ges[:,6]-273.15, label = "33 mm")#, markersize = 1)
        ln4, = plt.plot(narray, u_ges[:,7]-273.15, label = "37 mm")#, markersize = 1)  
        vln = plt.axvline(x=q, color='black', linestyle='--', label='now')
        print("size of uges")
        print(u_ges.size)
        #time.sleep(6)
        print("size of uges reported")
        
        plt.legend()
        
        #for i in range(3):
        #    theta = np.random.uniform(0,360,10)
        #    r = np.random.uniform(0,1,10)
        #    ax.plot(theta,r,linestyle="None",marker='o', color=c[i])
        #    #canvas.draw()
        return[ln1,ln2,ln3,ln4, vln]
    
def savePlot(filename):
    plt.savefig(filename) 