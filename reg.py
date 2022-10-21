"""
Main Datei

"""
import numpy as np
import materialparameter as m
import reaktionskinetik as r
import wärmeleitung as w
import write
import time
import warnings


#U GES[:SCLICER] = U_GES [SLICER] damit nicht vorherige WERTE bernommen werden können!!!
#TODO: MAX UND MIN ALPHA AUSGEBEN.

#u_ges leer mit Anfangstemperatur und Temperaturkurve
#nsteps steps in die Zukunft
#U-ges rausschreiben
#Neu rechnen, u_ges von 100 sekunden nehmen, u[0] und temperaturrampe neu definieren
#Steps widerholen 

#switchH acts as a "lever"; while False, the Heattransfer coefficiant is calculated
#if it's True the HTC is adjusted to match a "fleece" on the object
switchH = False
T_out = 18.4
#u_init = 39  # used in wärmeleitung.py
h_luft_covered = None #4
alpha_start = None #0.04 #0.0000001 #0.00000001
phi = None

def set_u_init(T):
    w.u_init = T ################
    
def get_u_init():
    return w.u_init  #################
    
def set_layer_composition(core): # set core? set thickness? set boundaries??
    # set it in m:
    m.density_core, m.c_core, m.k_core = m.materialParam(core)
    ## set in r:
    #r.set_layer_composition(core)
    # set in w:
    w.set_layer_composition(core)
    
#def get_layer_composition():
#    pass
#    #return None #reg.get_u_init()  #################

def setVal(ny, nsteps, dt, dy2, **kwargs ):
    global alpha_start
    
    phi=None

    if "alpha_start" in kwargs:
        alpha_start=kwargs["alpha_start"]
        
    if "phi" in kwargs:
        phi=kwargs["phi"]
    
    u0, u, u_ges, u_left = w.uArrays(ny, nsteps)

    a_balsa, aa_balsa = m.calcDiffusivityBalsa(dt, dy2)

    u0, u, u_ges = w.celius_to_kelvin(u0, u, u_ges)
    
    k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges = r.reakArrays(ny, nsteps, dt=dt, alpha_start=alpha_start)
    
    density_schicht, c_schicht, k_schicht, phi, density_M = m.calcVerbund(phi=phi)
    
    h_luft_ges = np.ones((nsteps, ny))
    
    #testwert = (k_schicht/(density_schicht * c_schicht)) * (dt / dy2)

    #print("Der Testwert beträgt: " + str(testwert) + " sollte unter 0.5 sein!")
    
    return (u0, u, u_ges, u_left, a_balsa, aa_balsa, u0, u, u_ges, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, density_M, h_luft_ges) # u_left is in celsius but u0, u and u_ges in kelvin?

def timestep_lam(u0, u, u_ges, u_left, a_balsa, aa_balsa, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges, nsteps, dy, dt, dy2, ny, boundary1, boundary2, **kwargs):
    global alpha_start, h_luft_covered

    if "alpha_start" in kwargs:
        alpha_start=kwargs["alpha_start"]
    
    if "mat_layers" in kwargs:
        mat_layers=kwargs["mat_layers"]
    else:
        mat_layers="default"
        import warnings
        warnings.warn("layer composition not defined, default value is used")
        raise ValueError('please define layer composition', 'x', 'y')
        
    a_schicht, aa_schicht, density_schicht, k_comp, cp_comp = m.calcSchichtT(ny, alpha, u, dt, dy2, phi=phi)
    
    if 2*np.max(a_schicht) > dy2/dt:
        print("2aaschicht: "+str(2*np.max(aa_schicht)))
        print("dy2/dt"+str(dy2/dt))
        #raise ValueError('stability condition not fulfilled', 'np.max(aa_schicht)', 'dt')
        warnings.warn("stability condition not fulfilled")
        
    # Kamal-Souror method
    #print("timestep dadt0: "+str(dadt0))
    reak_kinetic, alpha, dadt, Tg = r.calcReaktionskinetik(ny, dt,  phi, density_M, 
                         density_schicht, u0, u, 1, -1, nsteps, alpha0, dadt0)  
    if( (dadt*dt>1).any() ):
        print("dt:"+str(dt))
        print("dadt:"+str(dadt))
        #print("alpha0:"+str(alpha0))
        raise ValueError("dt is "+str(dt)+", dadt is >1: "+str(dadt))
    
    if mat_layers not in ['only fibre layers','with balsa core', 'with foam core', 'default']:
        raise ValueError('mat_layers not permitted', 'x', 'y')

        
    if "printu" in kwargs:
        if kwargs["printu"] == True:
            print("u_ges[8]_inside_lam1: "+str(u_ges[8]))
            
    #print("h_luft_covered:"+str(h_luft_covered))
    u, h_luft = w.robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp, switchH=switchH, T_out=T_out, h_luft_covered = h_luft_covered)
    
    #print("u after robin Boundary"+str(u))

    if mat_layers in ['with balsa core','with foam core']:
        #interface boundaries are needed
        ##print("boundaries are "+str(boundary1)+" and "+str(boundary2))
        u0[boundary1] = w.interfaceBoundary1(aa_schicht, aa_balsa, u0, boundary1)   
        u0[boundary2] = w.interfaceBoundary2(aa_schicht, aa_balsa, u0, boundary2) 
        # save values also to u
        u[boundary1] = u0[boundary1]
        u[boundary2] = u0[boundary2]    
        ##print("boundaries u0: ", str(u0[boundary1]), str(u0[boundary1]))
        ##print("manual u: ", str( u0[boundary1]+aa_schicht[boundary1]*(u0[boundary1+1]+u0[boundary1-1]-2*u0[boundary1]) ))
        ##print("manual u_all: ", str( u0[1:boundary1+1-1] + aa_schicht[1:boundary1+1-1] * (u0[1+1:boundary1+1] - 2*u0[1:boundary1+1-1] + u0[1-1:boundary1+1-2]) ))  ####u0[leftB:rightB-1] + a[leftB:rightB-1] * (u0[leftB+1:rightB] - 2*u0[leftB:rightB-1] + u0[leftB-1:rightB-2])
        u = w.calcU1(u, u0, aa_schicht, 1, boundary1+1)
        ##print("boundaries u: ", str(u[boundary1]), str(u[boundary1]))
        u[1 : boundary1] += reak_kinetic[1 : boundary1]
        u = w.calcU2(u, u0, aa_balsa, boundary1+1, boundary2+1) 
        u = w.calcU3(u, u0, aa_schicht, boundary2+1, -1)
        u[boundary2+1:-1] += reak_kinetic[boundary2+1:-1]
            
        ##print("boundaries u-1: ", str(u[boundary1-1]), str(u[boundary1-1]))

    if "printu" in kwargs:
        if kwargs["printu"] == True:
            print("u_ges[8]_inside_lam2: "+str(u_ges[8]))

    #u, h_luft = w.robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp, switchH=switchH, T_out=T_out)
    
    if "printu" in kwargs:
        if kwargs["printu"] == True:
            print("u_ges[8]_inside_lam3: "+str(u_ges[8]))
    
    if mat_layers in ['only fibre layers', 'default']:
        # without interface boundaries
        #print("reak_kinetic "+str(reak_kinetic))
        #print("u before"+str(u))
        u[1 : -1] += reak_kinetic[1 : -1]#+20
        #print("u after10"+str(u))
        if "printu" in kwargs:
            if kwargs["printu"] == True:
                print("u_ges[8]_inside_lam3BBB: "+str(u_ges[8]))
                
        ### ACHTUNG: w.calcU überschreibt wieder die Änderungen durch die Reaktionskinetik!!!!!!!!
        u0neu=np.copy(u) ##experimentell:
        u = w.calcU(u, u0neu, aa_schicht, 1, -1) #u = w.calcU(u, u0, aa_schicht, 1, -1) 
        
        #print("u afterw"+str(u))
        
        #print("u after calcU"+str(u))
    
            
    if "printu" in kwargs:
        if kwargs["printu"] == True:
            print("u_ges[8]_inside_lam4: "+str(u_ges[8]))
    
    reak_kinetic_ges[-1] = reak_kinetic
    h_luft_ges[-1] = h_luft  
        
    # this function messes the last index of u_ges up - dont use the u_ges that is returned here
    
        
    return u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges, alpha, dadt

# this function shall replace regelung1 and regelung2 -> has to be unified more
def controlStep(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, **kwargs):   ##### plus / minus
    # if first controlStep: q = None, eingegeben=eingeben1, slicer=None, oldslice=None
    global alpha_start, phi

    if "alpha_start" in kwargs:
        alpha_start=kwargs["alpha_start"]

    if "phi" in kwargs:
        phi=kwargs["phi"]
    
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
    
    if "prefix" in kwargs:
        prefix=kwargs["prefix"]
    else:
        prefix=""
        
    if "layers" in kwargs:
        mat_layers=kwargs["layers"]
    else:
        mat_layers="default"
        
    if "first" in kwargs:
        first=kwargs["first"]
    else:
        first=False
        
    if "silent" in kwargs:
        silent=kwargs["silent"]
    else:
        silent=False
        
    if "plus" in kwargs:
        plus=kwargs["plus"]
    else:
        plus=0
    
    #print("eingegeben: "+str(eingegeben)+" plus: " + str(plus))
    
    print("controlstep with q="+str(q)+", first="+str(first)+"-----------------------------------")
    (u0, u, u_ges, u_left, a_balsa, aa_balsa, u0_DUMMY, u_DUMMY, u_ges_DUMMY, k1, k2,   # u_ges_DUMMY
     alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges) = setVal(ny, nsteps, dt, dy2 , alpha_start=alpha_start, phi=phi)    
     
    if first==False: #regelung2
        if "never"=="do this": #do_write:  # maybe this branch should be replaced / removed, to increase speed in any case
            u_ges_read, alpha_ges_read, dadt_ges_read = write.read(prefix=prefix)
            #print(u_ges_read.shape)
        else:
            if "u_ges" in kwargs:
                u_ges_read=kwargs["u_ges"]
            else:
                raise Exception("Error!, if do_write==False, u_ges has to be provided")
            if "alpha_ges" in kwargs:
                alpha_ges_read=kwargs["alpha_ges"]
            else:
                raise Exception("Error!, if do_write==False, alpha_ges has to be provided")
            if "dadt_ges" in kwargs:
                dadt_ges_read=kwargs["dadt_ges"]
            else:
                raise Exception("Error!, if do_write==False, dadt_ges has to be provided")
            #print(u_ges_read.shape)
        if q == 0:
            u_ges[:stepsprorechnung] = np.copy(u_ges_read)
            dadt_ges[:stepsprorechnung] = np.copy(dadt_ges_read)
            alpha_ges[:stepsprorechnung] = np.copy(alpha_ges_read)
        else:
            u_ges[:stepsprorechnung+oldslice] = np.copy(u_ges_read)
            dadt_ges[:stepsprorechnung+oldslice] = np.copy(dadt_ges_read)
            alpha_ges[:stepsprorechnung+oldslice] = np.copy(alpha_ges_read)
        
    if (plus>0):
        print("Maximaler Alpha + "+str(round(plus))+"°C: " + str(np.amax(alpha_ges[slicer])) + " Minimaler Alpha: " + str(np.amin(alpha_ges[slicer])))
    elif (plus<0):
        print("Maximaler Alpha - "+str(round(plus))+"°C: " + str(np.amax(alpha_ges[slicer])) + " Minimaler Alpha: " + str(np.amin(alpha_ges[slicer])))
    
    if first==True: # regelung1
        u0[0]  = eingegeben + plus                   ##### eingeben1 + plus  
        u[0] = eingegeben + plus #u0[0]               ##### np.copy(u0_PLUS[0])    
    elif first==False: #regelung2   
        u = np.copy(u_ges[slicer])   ###############
        u[0] = eingegeben + plus
        
        alpha = np.copy(alpha_ges[slicer])   ############
        dadt = np.copy(dadt_ges[slicer]) #########
        
    if first==True: # regelung1
        rangeslicer=0
    elif first==False: #regelung2
        rangeslicer=slicer
        
            
    for i in range(rangeslicer, stepsprorechnung+rangeslicer): # geht davon aus, das schon bis stelle slicer vorausberechnet/vorhergesagt wurde, sonst wohl fehler
        timeleft = dt
        #a_schicht, _, _, _, _ = m.calcSchichtT(ny, alpha, u, dt, dy2) # a_schicht is independent of dt
        #dttemp = min(dt,dy2/(2*np.max(a_schicht)))
        #print("timestep: "+str(dttemp))
        while timeleft > 0:  #for innnerI in range(int(1/dt)):
            a_schicht, aa_schicht, _, _, _ = m.calcSchichtT(ny, alpha, u, dt, dy2, phi=phi) # a_schicht is independent of dt
            #print("ideales dt ist "+str(dy2/(2*np.max(a_schicht))))
            dttemp = min(dt,dy2/(2*np.max(a_schicht)))  # aschicht * dt / dy^2 = aaschicht =>c aus Formel = aschicht/d^2 = aaschicht/dtnononononoonnoooooooooooooo    #0.001*
            #print("timestep: "+str(dttemp))
            timeleft -= dttemp
            #print(dy2)
            #print(a_schicht)
            #print(dttemp)
            
            #print("regelung1 dadt at i="+str(i)+": "+str(dadt))
            #print("step: "+str(i))
            alpha0 = np.copy(alpha)  #####           ##### alpha0_PLUS = alpha_PLUS
            dadt0 = np.copy(dadt)   ######           ##### dadt0_PLUS = dadt_PLUS
            u0 = np.copy(u)   ##########    ##### u0_PLUS = np.copy(u_PLUS)
            
            u_ges_DUMMY, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges, alpha, dadt = timestep_lam(u0, u, u_ges, u_left, a_balsa, aa_balsa, k1, k2, 
                alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
                density_schicht, c_schicht, k_schicht, phi, 
                density_M, h_luft_ges, nsteps, dy, dttemp, dy2, ny, boundary1, boundary2, mat_layers=mat_layers, alpha_start=alpha_start)  ### DUMMY dt->dttemp  ##, printu=i<-11
            
            #print("regelung1 dadt at i="+str(i)+" after timestep: "+str(dadt))
            if (u <0).any():
                print("u0:"+str(u0))
                print("u:"+str(u))
                raise Exception("temperature in 0 is negative") ###############
      
        u_ges[i] = np.copy(u) ##########   ##### u_ges_PLUS[i] = u_PLUS
        alpha_ges[i] = np.copy(alpha)  ##           ##### alpha_ges_PLUS[i] = alpha_PLUS
        dadt_ges[i] = np.copy(dadt)     ##          ##### dadt_ges_PLUS[i] = dadt_PLUS  

        if first==True: # regelung1
            if i == 0:
                extracool = np.copy(u)        ##### extracool_PLUS = np.copy(u_PLUS)    
        elif first==False: #regelung2
            if i == slicer:
                u_speicherfehlerAusgleich = np.copy(u)          # u_speicherfehlerAusgleich IST extracool sinngemaess
                dadt_speicherfehlerAusgleich = np.copy(dadt)
                alpha_speicherfehlerAusgleich = np.copy(alpha)
                #print("np,copy wg 'Fehler' bei i="+str(i))
            

    if first==True: # regelung1
        if (u_ges[0] != extracool).any():  #(A==B).all() ##########
            u_ges[i] = extracool          ###index i 0   ##### u_ges_PLUS[0] = extracool_PLUS
            raise Exception("Error!, u_ges[0] != extracool shall not happen") ###############
    elif first==False: #regelung2
        if (u_ges[slicer] != u_speicherfehlerAusgleich).any():  #(A==B).all()
            u_ges[slicer] = u_speicherfehlerAusgleich
            print("Error!, u_ges[slicer] != u_speicherfehlerAusgleich shall not happen with ",str(u_speicherfehlerAusgleich))
            raise Exception("Error!, u_ges[slicer] != u_speicherfehlerAusgleich shall not happen with ",str(u_speicherfehlerAusgleich))
            
        dadt_ges[slicer] = np.copy(dadt_speicherfehlerAusgleich)  ###
        alpha_ges[slicer] = np.copy(alpha_speicherfehlerAusgleich)   ####         
    
    if first==True: # regelung1
        writeslicer=0
    elif first==False: #regelung2
        writeslicer=slicer
    #print("size of u_ges after regelung2: "+str(u_ges.shape))
    #print("size of u_ges_write after regelung2: "+str(np.copy(u_ges[:stepsprorechnung+slicer]).shape))
    if do_write:    
        u_ges_write = np.copy(u_ges[:stepsprorechnung+writeslicer])
        dadt_ges_write = np.copy(dadt_ges[:stepsprorechnung+writeslicer])
        alpha_ges_write = np.copy(alpha_ges[:stepsprorechnung+writeslicer])
        #print("size of u_ges after regelung1: "+str(u_ges.shape))
        #print("size of u_ges_write after regelung1: "+str(u_ges_write.shape))
        write.save(u_ges_write, alpha_ges_write, dadt_ges_write, prefix=prefix, plus=plus)
        
    if first==True: # regelung1
        #write.plot_heatmap2(nsteps, dt, u_ges[:nsteps])
        #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges, axis=0)) + " Sekunden, nach " + str(np.argmax(u_ges, axis=1)) + " mm." )
        #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges, axis=0)) + " Sekunden, nach " + str(np.argmax(u_ges, axis=1)) + " mm." )
        # print maximum predicted temperatures and position
        result = np.where(u_ges == np.amax(u_ges[:stepsprorechnung]))     ##### result = np.where(u_ges_PLUS == np.amax(u_ges_PLUS[:stepsprorechnung]))
        if (silent==False):
            if (plus==0):
                print("result in regelung1:")
                print(result)
                print("result[0] in regelung1:")
                print(result[0])
            else:
                if len(result[0] > 1):
                    print("wenn "+str('{0:+d}'.format(round(plus)))+ "°C: " + str(round(np.amax(u_ges[:stepsprorechnung])-273.15,3)) + " °C nach " + str(result[0][0]) + " Sekunden, bei " + str(result[1][0]) + " mm.")
                else:
                    print("wenn "+str('{0:+d}'.format(round(plus)))+ "°C: " + str(round(np.amax(u_ges[:stepsprorechnung])-273.15,3)) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
                        
        if len(result[0] == 5):
            result2 = result[0]
       #     print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(result2[0]) + " Sekunden, bei " + str(result2[1]) + " mm.")
        #else:
        #    print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
        #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges)) + " Sekunden, nach " + str(np.argmax(u_ges)) + " mm." )
        #write.colormap(u_ges, dadt)
        ##### WENN PLUS ##### print("wenn + "+str(int(plus))+ "°C: " + str(round(np.amax(u_ges_PLUS[:stepsprorechnung])-273.15,3)) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
    elif first==False: #regelung2
        if (silent==False):
            print("α_max: " + str(np.amax(alpha_ges[slicer])) + "\nα_min: " + str(np.amin(alpha_ges[slicer])))
        #Wann wird minimaler Alpha überall erreicht?:
        MinAlpha = np.amin(alpha_ges[slicer:])#, stepsprorechnung+slicer])
        WhereMinAlpha = np.where(alpha_ges == MinAlpha)
        result = np.where(u_ges == np.amax(u_ges[slicer:]))
        
        if MinAlpha > 0.8:
            if (silent==False):
                print("Aushärtegrad von " + str(MinAlpha) +  " wird erstmals nach " + str(WhereMinAlpha) + "erreicht.")
            
        if (silent==False):
            print("T_max: " + str(np.amax(u_ges[slicer:])-273.15))# + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.\n \n")
            if len(result[0] > 1):
                print("wenn "+str('{0:+d}'.format(round(plus)))+ "°C: " + str(round(np.amax(u_ges[:stepsprorechnung])-273.15,3)) + " °C nach " + str(result[0][0]) + " Sekunden, bei " + str(result[1][0]) + " mm.")
            else:
                print("wenn "+str('{0:+d}'.format(round(plus)))+ "°C: " + str(round(np.amax(u_ges[:stepsprorechnung])-273.15,3)) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
        #print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
        #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges)) + " Sekunden, nach " + str(np.argmax(u_ges)) + " mm." )

    return u_ges, alpha_ges, dadt_ges, u, u0
