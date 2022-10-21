"""
Main Datei

"""
import numpy as np
#import wärmeleitung as w
import write
import reg
import time
#import Einlesen as e
#import tkinter as tk
import datetime
import os
from write import testPlot, savePlot

class heatingPlateSimulation:
    ##global slicer, oldslice
    ##global str_clock, str_T_max, str_a_max, str_a_min, str_wenn_plus, str_wenn_minus
    #slicer = None
    #oldslice = None
    #str_clock = None
    #str_T_max = None
    #str_a_max = None
    #str_a_min = None
    #str_wenn_plus = None
    #str_wenn_minus = None
    ##experimental:
    ##global matplotax
    ##global matplotcanvas
    ##global matplotfigure
    #matplotax = None
    #matplotcanvas = None
    #matplotfigure = None
    
    #h = 0.034 #[m] # vorversuch 13; IWES Versuch 34
    #dy = 0.001#[m]
    #dt = 1
    #ny = int(h/dy)
    #dy2 = dy*dy
    ##Hier boundaries eingeben [in mm]:
    #boundary1 = None #int(7)
    #boundary2 = None #int((6.5+31.5))
    #nsteps1 = Sekunden =  int(10*60*60) # 10 hours
    #stepsprorechnung = int(1200) # 1200 sec = 20 min
    #nsteps = int(Sekunden/dt) # maximal duration for experiment ; 10 hours should be enough
    #alpha_start=0.01 # degree of hardening at beginning of simulation
    #phi=0.55                 # fiber volume content for gf laminates
    
    #maxerlaubteTemperatur = 80+273.15 #40 +273.15
    
    #plus = 20
    
    #documentation = []
    #np.array(documentation)  # nonsense, if you want to make an np.array, then: documentation=np.array(documentation)
    
    #plotlines=None
    
    #starttime_prefix = None
    #layer_composition = None
    
    ##k_core = None  #0.06 #0.06-0.0935
    ##density_core = None  #140
    ##c_core = None  #2720  
    
    ## def update_clock():
    ##     # get current time as text
    ##     current_time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    #     
    ##def set_matplotcanvas(x):
    ##    global matplotcanvas
    ##    matplotcanvas = x
    ##def set_matplotfigure(x):
    ##    global matplotfigure
    ##    matplotfigure = x
    
    def __init__(self, plateNr):
        self.plateNr = plateNr    # instance variable unique to each instance
        self.slicer = None
        self.oldslice = None
        self.str_clock = None
        self.str_T_max = None
        self.str_a_max = None
        self.str_a_min = None
        self.str_wenn_plus = None
        self.str_wenn_minus = None
        self.matplotax = None
        self.matplotcanvas = None
        self.matplotfigure = None
        self.h = 0.034 #[m] # vorversuch 13; IWES Versuch 34
        self.dy = 0.001#[m]
        self.dt = 1
        self.ny = int(self.h/self.dy)
        self.dy2 = self.dy*self.dy
        #Hier boundaries eingeben [in mm]:
        self.boundary1 = None #int(7)
        self.boundary2 = None #int((6.5+31.5))
        self.nsteps1 = Sekunden =  int(10*60*60) # 10 hours
        self.stepsprorechnung = int(1200) # 1200 sec = 20 min
        self.nsteps = int(Sekunden/self.dt) # maximal duration for experiment ; 10 hours should be enough
        self.alpha_start=0.01 # degree of hardening at beginning of simulation
        self.phi=0.55                 # fiber volume content for gf laminates
        self.maxerlaubteTemperatur = 80+273.15 #40 +273.15
        self.plus = 20
        self.plotlines=None
        self.starttime_prefix = None
        self.layer_composition = None
        #new
        self.u_ges = None
        self.u_ges_MINUS = None
        self.u_ges_PLUS = None
        self.alpha_ges = None
        self.alpha_ges_PLUS = None
        self.alpha_ges_MINUS = None
        self.dadt_ges = None
        self.dadt_ges_PLUS = None
        self.dadt_ges_MINUS = None
        self.u = None
        self.u_PLUS = None
        self.u_MINUS = None
        self.u0 = None
        self.u0_PLUS = None
        self.u0_MINUS = None
        self.documentation = []
        #self.lastTemperatures = [None, None]
        self.lastTemperature = None
        self.start = None
        self.starttime = None
        #self.channel = None
        self.figure = None
    
    def set_hswitch(self, switch):
        #print("regswitch is "+str(reg.switchH)+" and will be set to "+str(switch))
        reg.switchH = switch
    
    def get_hswitch(self):
        return reg.switchH
    
    def set_T_out(self, T):
        reg.T_out = float(T)
    
    def get_T_out(self):
        return reg.T_out  
    
    def set_u_init(self, T):
        reg.set_u_init(T)
    
    def get_u_init(self):
        return reg.get_u_init()
    
    def set_layer_composition(self, core):
        reg.set_layer_composition(core)
    
    def set_h_luft(self, T):
        reg.h_luft_covered = float(T)
    
    def set_alpha_start(self, alpha):
        #global alpha_start
        self.alpha_start = float(alpha)
    
    def set_fvc(self, x):
        #fvc = float(x)
        self.phi = float(x)
    
    def set_clock(self):
        #global str_clock
        self.str_clock = "Time since start: " + str(self.slicer) + " sec"
    
    def get_clock(self):
        #global str_clock
        return self.str_clock
    
    def set_T_max(self):
        #global u_ges
        #global str_T_max
        self.str_T_max = np.amax(self.u_ges[self.slicer:])-273.15
    
    def get_minus(self):
        return np.amax(self.u_ges_MINUS[self.slicer:])-273.15       
    
    def get_plus(self):
        return np.amax(self.u_ges_PLUS[self.slicer:])-273.15
    
    #def set_plus(plus):
    #    global plus
    #    plus = plus
    
    def get_T_max(self):
        #global str_T_max
        return self.str_T_max
    
    def set_a_max(self):
        #global alpha_ges
        #global str_a_max
        self.str_a_max = np.amax(self.alpha_ges[self.slicer])
    
    def get_a_max(self):
        #global str_a_max
        return self.str_a_max
    
    #def set_max_alpha():
    #    max_alpha_in_that_step = np.amax(alpha_ges[slicer:stepsprorechnung+slicer])
    
    def get_max_alpha(self):
        max_alpha_in_that_step = np.amax(self.alpha_ges[self.slicer:self.stepsprorechnung+self.slicer])
        return max_alpha_in_that_step
    
    def find_when_alpha_min(self):
        alpha_reached = 1
        alpha_reached_at = 1
        found_alpha = False
        for k in range(self.stepsprorechnung):
            if np.amin(self.alpha_ges[self.slicer+k,:]) >= 0.005:
                alpha_reached = np.amin(self.alpha_ges[self.slicer+k,:])
                alpha_reached_at = self.slicer+k
                found_alpha = True #not found_alpha
                break
        return alpha_reached, alpha_reached_at, found_alpha
    
    def set_a_min(self):
        #global alpha_ges
        #global str_a_min
        self.str_a_min = np.amin(self.alpha_ges[self.slicer])
    
    def get_a_min(self):
        #global str_a_min
        return self.str_a_min
    
    def get_alpha_min_PLUS(self):
        #global alpha_ges_PLUS, slicer
        return np.amin(self.alpha_ges_PLUS[self.slicer])
    
    def get_alpha_min_MINUS(self):
        #global alpha_ges_MINUS, slicer
        return np.amin(self.alpha_ges_MINUS[self.slicer])
    
    def get_alpha_max_PLUS(self):
        #global alpha_ges_PLUS, slicer
        return np.amax(self.alpha_ges_PLUS[self.slicer])
    
    def get_alpha_max_MINUS(self):
        #global alpha_ges_MINUS, slicer
        return np.amax(self.alpha_ges_MINUS[self.slicer])
    
    def set_wenn_plus(self):
        #global plus, u_ges_PLUS, slicer
        #global str_wenn_plus
        result = np.where(self.u_ges_PLUS == np.amax(self.u_ges_PLUS[self.slicer:]))
        if len(result[0]!=1) or len(result[1]!=1):
            self.str_wenn_plus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."
        else:
            #####str_wenn_plus = "after " + str(result[0][0]) + " sec, at " + str(result[1][0]) + " mm."
            self.str_wenn_plus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."
    
    def get_wenn_plus(self):
        #global str_wenn_plus
        return self.str_wenn_plus
    
    def set_wenn_minus(self):
        #global plus, u_ges_MINUS, slicer
        #global str_wenn_minus
        result = np.where(self.u_ges_MINUS == np.amax(self.u_ges_MINUS[self.slicer:]))
        if len(result[0]!=1) or len(result[1]!=1):
            self.str_wenn_minus = ":: after " + str(result[0]) + " sec, at " + str(result[1]) + " mm."
        else:
            self.str_wenn_minus = "after " + str(result[0][0]) + " sec, at " + str(result[1][0]) + " mm."
    
    def get_wenn_minus(self):
        #global str_wenn_minus
        return self.str_wenn_minus
    
    def get_delta_plus(self):
        return self.plus

    def do_once(self, eingegeben, active_channel, **kwargs):
        #global u_ges, alpha_ges, dadt_ges, u, u0
        #global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
        #global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
        #global plus#, slicer, oldslice, q
        #global nsteps, dy, dt, dy2, ny, boundary1, boundary2, stepsprorechnung #, eingegeben1
        #global documentation  ###### globale liste oder klassenattribut
        #global slicer, oldslice
        #global plotlines
        #global starttime_prefix, layer_composition
        #global alpha_start, phi
        if "do_plot" in kwargs:
            do_plot=kwargs["do_plot"]
        else:
            do_plot = True
        
        ##eingegeben1 = e.getTemperature(10)   
        ##eingegeben.insert(0, 0) # wenn liste, dann 0 an position 0 schreiben???
        ######## globale liste oder klassenattribut #############################
        ##documentation.append(tuple(eingegeben))  #((0,eingegeben)) #documentation.append((0,eingegeben1))
        self.documentation.append((0,eingegeben))
        #temperature = eingegeben[active_channel]   #active channel könnte als klassenattribut funktionieren !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        temperature = eingegeben
        self.lastTemperature = temperature
        start = time.time()
        self.start = start
        print("temperature in maindo: "+str(temperature))
        self.u_ges, self.alpha_ges, self.dadt_ges, self.u, self.u0 = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, None, temperature, None, self.stepsprorechnung, None, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition, first=True, alpha_start=self.alpha_start, phi=self.phi) 
        self.u_ges_PLUS, self.alpha_ges_PLUS, self.dadt_ges_PLUS, self.u_PLUS, self.u0_PLUS = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, None, temperature, None, self.stepsprorechnung, None, plus=self.plus, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition, first=True, alpha_start=self.alpha_start, phi=self.phi) 
        self.u_ges_MINUS, self.alpha_ges_MINUS, self.dadt_ges_MINUS, self.u_MINUS, self.u0_MINUS = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, None, temperature, None, self.stepsprorechnung, None, plus=-self.plus, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition, first=True, alpha_start=self.alpha_start, phi=self.phi) 
                                                          
        self.plus = (self.maxerlaubteTemperatur - np.amax(self.u_ges))/2
        if self.plus < 0:
            self.plus = 0
        print("Temperaturzuschlag/abzug für Parallelrechnungen: "+str(self.plus)) #Temperaturzuschlag/abzug für Parallelrechnungen
        #write.animatePlot(u_ges[:stepsprorechnung], stepsprorechnung)   
        #global matplotcanvas, matplotax
        self.plotlines = testPlot(self.matplotfigure, self.matplotax,self.u_ges[:self.stepsprorechnung], self.stepsprorechnung, 0)
        print(self.plotlines)
        self.slicer = 0
        self.oldslice = 0
        self.q = -1
        return self.q, self.start, self.plus  # könnte start auch in klassenvariabler festlegen
    
    # function (oneliner) to clear the console:
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    def do_process(self, q, start, starttime, eingegeben, active_channel, **kwargs): #, plus ???????????? ist das plus nicht notwendig für mainWindowTK??????????
        #clearConsole()
        #global u_ges, alpha_ges, dadt_ges, u, u0
        #global u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS 
        #global u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS
        #global plus#, slicer, oldslice, q
        #global nsteps, dy, dt, dy2, ny, boundary1, boundary2, stepsprorechnung #, eingegeben1
        #global documentation
        #global slicer, oldslice
        #global matplotcanvas, matplotax
        #global plotlines, matplotfigure
        #global starttime_prefix, layer_composition
        #global alpha_start, phi
        if "do_plot" in kwargs:
            do_plot=kwargs["do_plot"]
        else:
            do_plot = True
        
        if "matplotfigure" in kwargs:
            matplotfigure=kwargs["matplotfigure"]
        else:
            matplotfigure = self.matplotfigure
            
        if "matplotax" in kwargs:
            matplotax=kwargs["matplotax"]
        else:
            matplotax = self.matplotax
            
        #self.matplotfigure, self.matplotax
        
        self.q += 1  
        
        endtime = time.time()
        #matplotax.clear()
        if self.q == 0:   
            dif1 = int(endtime-start)  # oder self.start !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #dif1 = int(input("Slicer"))
            print("Verstrichende Zeit in Sekunden: " + str(dif1) + "- slicer is: "+str(self.slicer)+" active-ch: " +str(active_channel))
            self.slicer += dif1 # # slicer was 0 and is noch dif1?
        else: 
            #Die entfernten Zeilen müssen in der TKinter Datei angepasst werden --> "Schalter"Funktion die durch button klick ausgelöst wird
            self.oldslice = self.slicer
            self.slicer += int(endtime-starttime)
            #slicer = int(input("Slicer"))
            print("Verstrichende Zeit in Sekunden: " + str(self.slicer))
            
        #eingegeben.insert(0, slicer)
        #documentation.append(tuple(eingegeben))  #documentation.append((slicer, eingegeben))    
        self.documentation.append((self.slicer, eingegeben))   
        #temperature = eingegeben[active_channel]
        temperature = eingegeben
        self.lastTemperature = temperature
        starttime = time.time()
        self.plus = (self.maxerlaubteTemperatur - np.amax(self.u_ges))/2 
        if self.plus < 1: #0: # lower steps than 1 degree probably not useful
            self.plus = 1 # 0
        
        # prefix: prefix=f"{self.starttime_prefix}_ch{self.plateNr}_"
        print("self.stepsprorechnung+self.oldslice: "+str(self.stepsprorechnung) +" + "+str(self.oldslice))
        self.u_ges, self.alpha_ges, self.dadt_ges, self.u, self.u0 = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, self.q, temperature, self.slicer, self.stepsprorechnung, self.oldslice, 
                                                            write=False, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition, 
                                                            u_ges=self.u_ges[:self.stepsprorechnung+self.oldslice], 
                                                            alpha_ges=self.alpha_ges[:self.stepsprorechnung+self.oldslice], 
                                                            dadt_ges=self.dadt_ges[:self.stepsprorechnung+self.oldslice],                                      
                                                            first=False, silent=False, alpha_start=self.alpha_start, phi=self.phi)
        self.set_a_max()
        self.set_a_min()
        #set_max_alpha()
        self.u_ges_PLUS, self.alpha_ges_PLUS, self.dadt_ges_PLUS, self.u_PLUS,self.u0_PLUS = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, self.q, temperature,self.slicer, self.stepsprorechnung, self.oldslice, 
                                                                                    plus=self.plus, write=False, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition, 
                                                                                    u_ges=self.u_ges_PLUS[:self.stepsprorechnung+self.oldslice], 
                                                                                    alpha_ges=self.alpha_ges_PLUS[:self.stepsprorechnung+self.oldslice], 
                                                                                    dadt_ges=self.dadt_ges_PLUS[:self.stepsprorechnung+self.oldslice],                                      
                                                                                    first=False, silent=True, alpha_start=self.alpha_start, phi=self.phi)
        self.set_wenn_plus()
        self.u_ges_MINUS, self.alpha_ges_MINUS, self.dadt_ges_MINUS, self.u_MINUS, self.u0_MINUS = reg.controlStep(self.nsteps, self.dy, self.dt, self.dy2, self.ny, self.boundary1, self.boundary2, self.q, temperature,self.slicer, self.stepsprorechnung, self.oldslice, 
                                                                                    plus=-self.plus, write=False, prefix=f"{self.starttime_prefix}_ch{self.plateNr}_", layers=self.layer_composition,
                                                                                    u_ges=self.u_ges_MINUS[:self.stepsprorechnung+self.oldslice], 
                                                                                    alpha_ges=self.alpha_ges_MINUS[:self.stepsprorechnung+self.oldslice], 
                                                                                    dadt_ges=self.dadt_ges_MINUS[:self.stepsprorechnung+self.oldslice],                                      
                                                                                    first=False, silent=True, alpha_start=self.alpha_start, phi=self.phi)
        self.set_clock()
        self.set_T_max()
        self.set_wenn_minus()
        #result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[slicer:]))
        # str_wenn_minus = "wenn - "+str(int(plus))+ "°C: " + str(np.amax(u_ges_MINUS[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm."
        # bsser am anfang?
        #plus = (maxerlaubteTemperatur - np.amax(u_ges))/2 # wird erst beim nächsten update für regelung2 verwendet
        #if plus < 0:
        #    plus = 0
        #print(plus)
        #write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer)    
        #time.sleep(0.1)
        if do_plot:
            testPlot(matplotfigure, matplotax,self.u_ges[:self.stepsprorechnung+self.slicer], self.stepsprorechnung+self.slicer, self.slicer, update=self.plotlines, channel=str(active_channel)) #self.matplotfigure, self.matplotax ## self.plateNr  statt cgannel!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        #savePlot("regelung-plot.svg") # does not show up if not saved...
            
        return self.q, self.plus, starttime           
    #write.plot_heatmap2(stepsprorechnung+slicer, dt, u_ges[:stepsprorechnung+slicer])

    def end_process(self, **kwargs):
        #global documentation, stepsprorechnung
        #global slicer, q
        #global starttime_prefix, layer_composition
        if "do_plot" in kwargs:
            do_plot=kwargs["do_plot"]
        else:
            do_plot = True
            
        if "matplotfigure" in kwargs:
            matplotfigure=kwargs["matplotfigure"]
        else:
            matplotfigure = self.matplotfigure
            
        if "matplotax" in kwargs:
            matplotax=kwargs["matplotax"]
        else:
            matplotax = self.matplotax
            
        print(self.documentation)
        np.savetxt(f"{self.starttime_prefix}_ch{self.plateNr}_documentation.csv", self.documentation)
        write.save(self.u_ges[:self.stepsprorechnung+self.slicer], self.alpha_ges[:self.stepsprorechnung+self.slicer], self.dadt_ges[:self.stepsprorechnung+self.slicer], prefix=f"{self.starttime_prefix}_ch{self.plateNr}_")
        #write.animatePlot(u_ges[:stepsprorechnung+slicer], stepsprorechnung+slicer) 
        #global matplotcanvas, matplotax
        if do_plot:
            testPlot(matplotfigure, matplotax,self.u_ges[:self.stepsprorechnung+self.slicer], self.stepsprorechnung+self.slicer, self.slicer, update=self.plotlines, channel=str(self.plateNr))
        
        savePlot(f"{self.starttime_prefix}_ch{self.plateNr}_regelung-plot.svg")
        #print(self.documentation)