"""
Main Datei

"""
import numpy as np
import materialparameter as m
import reaktionskinetik as r
import wärmeleitung as w
import write
import time



#U GES[:SCLICER] = U_GES [SLICER] damit nicht vorherige WERTE bernommen werden können!!!
#TODO: MAX UND MIN ALPHA AUSGEBEN.

#u_ges leer mit Anfangstemperatur und Temperaturkurve
#nsteps steps in die Zukunft
#U-ges rausschreiben
#Neu rechnen, u_ges von 100 sekunden nehmen, u[0] und temperaturrampe neu definieren
#Steps widerholen 


def setVal(ny, nsteps, dt, dy2 ):
    
    u0, u, u_ges, u_left = w.uArrays(ny, nsteps)

    a_balsa, aa_balsa = m.calcDiffusivityBalsa(dt, dy2)

    u0, u, u_ges = w.celius_to_kelvin(u0, u, u_ges)
    
    k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges = r.reakArrays(ny, nsteps)
    
    density_schicht, c_schicht, k_schicht, phi, density_M = m.calcVerbund()
    
    h_luft_ges = np.ones((nsteps, ny))
    
    #testwert = (k_schicht/(density_schicht * c_schicht)) * (dt / dy2)

    #print("Der Testwert beträgt: " + str(testwert) + " sollte unter 0.5 sein!")
    
    return (u0, u, u_ges, u_left, a_balsa, aa_balsa, u0, u, u_ges, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, density_M, h_luft_ges)

def timestep_lam(u0, u, u_ges, u_left, a_balsa, aa_balsa, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges, nsteps, dy, dt, dy2, ny, boundary1, boundary2):
        
    a_schicht, aa_schicht, density_schicht, k_comp, cp_comp = m.calcSchichtT(ny, alpha, u, dt, dy2)
        
    #regular Kamal-Souror method
    #reak_kinetic, alpha, dadt = r.calcReaktionskinetik(ny, dt,  phi, density_M, 
    #                     density_schicht, u0, u, 1, -1, nsteps, alpha0, dadt0)  
    #advanced Kamal-Souror method
    reak_kinetic, alpha, dadt, Tg = r.calcReaktionskinetik_135(ny, dt,  phi, density_M, 
                         density_schicht, u0, u, 1, -1, nsteps, alpha0, dadt0)  
    #interface boundaries
    #u0[boundary1] = w.interfaceBoundary1(aa_schicht, aa_balsa, u0, boundary1)   
    #u0[boundary2] = w.interfaceBoundary2(aa_schicht, aa_balsa, u0, boundary2)     
    #u = w.calcU1(u, u0, aa_schicht, 1, boundary1+1) 
    #u[1 : boundary1] += reak_kinetic[1 : boundary1]
    #u = w.calcU2(u, u0, aa_balsa, boundary1+1, boundary2+1) 
    #u = w.calcU3(u, u0, aa_schicht, boundary2+1, -1)
    #u[boundary2+1:-1] += reak_kinetic[boundary2+1:-1]


    u, h_luft = w.robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp)
    
    # without interface boundaries
    u[1 : -1] += reak_kinetic[1 : -1]
    u = w.calcU(u, u0, aa_schicht, 1, -1) 
    
    reak_kinetic_ges[-1] = reak_kinetic
    h_luft_ges[-1] = h_luft  
        
    return u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges, alpha, dadt


def regelung1(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingeben1, stepsprorechnung, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
    
    (u0, u, u_ges, u_left, a_balsa, aa_balsa, u0, u, u_ges, k1, k2, 
     alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges) = setVal(ny, nsteps, dt, dy2 )    
   
    u0[0]  = eingeben1
    u[0] = u0[0]

    for i in range(stepsprorechnung):
       
        alpha0 = alpha
        dadt0 = dadt
        
        u0 = u
        
        u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges, alpha, dadt = timestep_lam(u0, u, u_ges, u_left, a_balsa, aa_balsa, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges[i] = u
        alpha_ges[i] = alpha
        dadt_ges[i] = dadt  
    
    u_ges_write = np.copy(u_ges[:stepsprorechnung])
    dadt_ges_write = np.copy(dadt_ges[:stepsprorechnung])
    alpha_ges_write = np.copy(alpha_ges[:stepsprorechnung]) 
    if do_write:
        write.save(u_ges_write, alpha_ges_write, dadt_ges_write)
    
    #write.plot_heatmap2(nsteps, dt, u_ges[:nsteps])
    #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges, axis=0)) + " Sekunden, nach " + str(np.argmax(u_ges, axis=1)) + " mm." )
    result = np.where(u_ges == np.amax(u_ges[:stepsprorechnung]))
    if len(result[0] == 5):
        result2 = result[0]
   #     print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(result2[0]) + " Sekunden, bei " + str(result2[1]) + " mm.")
    #else:
    #    print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
    #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges)) + " Sekunden, nach " + str(np.argmax(u_ges)) + " mm." )
    #write.colormap(u_ges, dadt)
    return u_ges, alpha_ges, dadt_ges, u, u0

def regelung2(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
   
    
    (u0, u, u_ges, u_left, a_balsa, aa_balsa, u0, u, u_ges, k1, k2, 
     alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges) = setVal(ny, nsteps, dt, dy2 )
    
    u_ges_read, alpha_ges_read, dadt_ges_read = write.read()
    #print(u_ges_read.shape)
    if "u_ges" in kwargs:
        u_ges_read=kwargs["u_ges"]
    if "alpha_ges" in kwargs:
        alpha_ges_read=kwargs["alpha_ges"]
    if "dadt_ges" in kwargs:
        dadt_ges_read=kwargs["dadt_ges"]
    #print(u_ges_read.shape)
    if q == 0:
        u_ges[:stepsprorechnung] = np.copy(u_ges_read)
        dadt_ges[:stepsprorechnung] = np.copy(dadt_ges_read)
        alpha_ges[:stepsprorechnung] = np.copy(alpha_ges_read)
    else:
        u_ges[:stepsprorechnung+oldslice] = np.copy(u_ges_read)
        dadt_ges[:stepsprorechnung+oldslice] = np.copy(dadt_ges_read)
        alpha_ges[:stepsprorechnung+oldslice] = np.copy(alpha_ges_read)
        
   
    
    
    u = u_ges[slicer]   
    u[0] = eingegeben
    
    alpha = alpha_ges[slicer]
    dadt = dadt_ges[slicer]

    
    for i in range(slicer, stepsprorechnung+slicer):
        
        alpha0 = alpha
        dadt0 = dadt
        u0 = u
        #u0 = u_ges[i-1]
        
        u_ges, u0, u, alpha_ges, dadt_ges, reak_kinetic_ges, h_luft_ges, alpha, dadt = timestep_lam(u0, u, u_ges, u_left, a_balsa, aa_balsa, k1, k2, 
            alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges[i] = u  
        alpha_ges[i] = alpha
        dadt_ges[i] = dadt     
        
        if i == slicer:
            u_speicherfehlerAusgleich = np.copy(u)
            dadt_speicherfehlerAusgleich = np.copy(dadt)
            alpha_speicherfehlerAusgleich = np.copy(alpha)
            
    u_ges[slicer] = u_speicherfehlerAusgleich
    dadt_ges[slicer] = dadt_speicherfehlerAusgleich
    alpha_ges[slicer] = alpha_speicherfehlerAusgleich
    
    u_ges_write = np.copy(u_ges[:stepsprorechnung+slicer])
    dadt_ges_write = np.copy(dadt_ges[:stepsprorechnung+slicer])
    alpha_ges_write = np.copy(alpha_ges[:stepsprorechnung+slicer])
    
    if do_write:
        write.save(u_ges_write, alpha_ges_write, dadt_ges_write)
    print("α_max: " + str(np.amax(alpha_ges[slicer])) + "\nα_min: " + str(np.amin(alpha_ges[slicer])))
    #Wann wird minimaler Alpha überall erreicht?:
    MinAlpha = np.amin(alpha_ges[slicer:])#, stepsprorechnung+slicer])
    WhereMinAlpha = np.where(alpha_ges == MinAlpha)
    result = np.where(u_ges == np.amax(u_ges[slicer:]))
    
    if MinAlpha > 0.8:
        print("Aushärtegrad von " + str(MinAlpha) +  " wird erstmals nach " + str(WhereMinAlpha) + "erreicht.")
    print("T_max: " + str(np.amax(u_ges[slicer:])-273.15))# + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.\n \n")
    #print("Maximale vorkommende Temperatur: " + str(np.amax(u_ges[slicer:])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
    #print("Maximale vorkommende Temperatur: "+ str(np.amax(u_ges[:stepsprorechnung])-273.15) + " °C nach " + str(np.argmax(u_ges)) + " Sekunden, nach " + str(np.argmax(u_ges)) + " mm." )

    return u_ges, alpha_ges, dadt_ges, u, u0


def regelung1_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingeben1, stepsprorechnung, plus, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
   
    
    (u0_PLUS, u_PLUS, u_ges_PLUS, u_left_PLUS, a_balsa, aa_balsa, u0_PLUS, u_PLUS, u_ges_PLUS, k1, k2, 
     alpha_PLUS, alpha0_PLUS, dadt_PLUS, dadt0_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges_PLUS) = setVal(ny, nsteps, dt, dy2)    
   
    u0_PLUS[0]  = eingeben1 + plus
    u_PLUS[0] = u0_PLUS[0]
    
    for i in range(stepsprorechnung):
        
        alpha0_PLUS = alpha_PLUS
        dadt0_PLUS = dadt_PLUS
        
        u0_PLUS = u_PLUS
        
        u_ges_PLUS, u0_PLUS, u_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, h_luft_ges_PLUS, alpha_PLUS, dadt_PLUS = timestep_lam(u0_PLUS, u_PLUS, u_ges_PLUS, u_left_PLUS, a_balsa, aa_balsa, k1, k2, 
            alpha_PLUS, alpha0_PLUS, dadt_PLUS, dadt0_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges_PLUS, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges_PLUS[i] = u_PLUS
        alpha_ges_PLUS[i] = alpha_PLUS
        dadt_ges_PLUS[i] = dadt_PLUS  
        
    u_ges_PLUS_write = np.copy(u_ges_PLUS[:stepsprorechnung])
    dadt_ges_PLUS_write = np.copy(dadt_ges_PLUS[:stepsprorechnung])
    alpha_ges_PLUS_write = np.copy(alpha_ges_PLUS[:stepsprorechnung]) 
    if do_write:
        write.save_PLUS(u_ges_PLUS_write, alpha_ges_PLUS_write, dadt_ges_PLUS_write)
    
    result = np.where(u_ges_PLUS == np.amax(u_ges_PLUS[:stepsprorechnung]))
    """
    if len(result[0] > 1):
        result2 = result[0]
        print("wenn +5°C: " + str(np.amax(u_ges_PLUS[:stepsprorechnung])-273.15) + " °C nach " + str(result2[0]) + " Sekunden, bei " + str(result2[1]) + " mm.")
    else:
        """
    print("wenn + "+str(int(plus))+ "°C: " + str(np.amax(u_ges_PLUS[:stepsprorechnung])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
    
    #print("wenn +5°C: " + str(np.amax(u_ges_PLUS)-273.15) + " °C")
    return u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS

def regelung1_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, eingeben1, stepsprorechnung, plus, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
   
    
    (u0_MINUS, u_MINUS, u_ges_MINUS, u_left_MINUS, a_balsa, aa_balsa, u0_MINUS, u_MINUS, u_ges_MINUS, k1, k2, 
     alpha_MINUS, alpha0_MINUS, dadt_MINUS, dadt0_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges_MINUS) = setVal(ny, nsteps, dt, dy2)    
   
    u0_MINUS[0]  = eingeben1 - plus
    u_MINUS[0] = u0_MINUS[0]
    
    for i in range(stepsprorechnung):
        
        alpha0_MINUS = alpha_MINUS
        dadt0_MINUS = dadt_MINUS
        
        u0_MINUS = u_MINUS
        
        u_ges_MINUS, u0_MINUS, u_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, h_luft_ges_MINUS, alpha_MINUS, dadt_MINUS = timestep_lam(u0_MINUS, u_MINUS, u_ges_MINUS, u_left_MINUS, a_balsa, aa_balsa, k1, k2, 
            alpha_MINUS, alpha0_MINUS, dadt_MINUS, dadt0_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges_MINUS, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges_MINUS[i] = u_MINUS
        alpha_ges_MINUS[i] = alpha_MINUS
        dadt_ges_MINUS[i] = dadt_MINUS  
        
    u_ges_MINUS_write = np.copy(u_ges_MINUS[:stepsprorechnung])
    dadt_ges_MINUS_write = np.copy(dadt_ges_MINUS[:stepsprorechnung])
    alpha_ges_MINUS_write = np.copy(alpha_ges_MINUS[:stepsprorechnung]) 
    if do_write:
        write.save_MINUS(u_ges_MINUS_write, alpha_ges_MINUS_write, dadt_ges_MINUS_write)
    
    result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[:stepsprorechnung]))
    """
    if len(result[0] > 1):
        result2 = result[0]
        print("wenn +5°C: " + str(np.amax(u_ges_MINUS[:stepsprorechnung])-273.15) + " °C nach " + str(result2[0]) + " Sekunden, bei " + str(result2[1]) + " mm.")
    else:
        """
    print("wenn - "+str(int(plus))+ "°C: " + str(np.amax(u_ges_MINUS[:stepsprorechnung])-273.15) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
    
    #print("wenn +5°C: " + str(np.amax(u_ges_MINUS)-273.15) + " °C")
    return u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS

def regelung2_PLUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
   
    
    (u0_PLUS, u_PLUS, u_ges_PLUS, u_left_PLUS, a_balsa, aa_balsa, u0_PLUS, u_PLUS, u_ges_PLUS, k1, k2, 
     alpha_PLUS, alpha0_PLUS, dadt_PLUS, dadt0_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges_PLUS) = setVal(ny, nsteps, dt, dy2) 
    
    u_ges_PLUS_read, alpha_ges_PLUS_read, dadt_ges_PLUS_read = write.read_PLUS()
    if "u_ges_PLUS" in kwargs:
        u_ges_PLUS_read=kwargs["u_ges_PLUS"]
    if "alpha_ges_PLUS" in kwargs:
        alpha_ges_PLUS_read=kwargs["alpha_ges_PLUS"]
    if "dadt_ges_PLUS" in kwargs:
        dadt_ges_PLUS_read=kwargs["dadt_ges_PLUS"]
    
    if q == 0:
        u_ges_PLUS[:stepsprorechnung] = np.copy(u_ges_PLUS_read)
        dadt_ges_PLUS[:stepsprorechnung] = np.copy(dadt_ges_PLUS_read)
        alpha_ges_PLUS[:stepsprorechnung] = np.copy(alpha_ges_PLUS_read)
    else:
        u_ges_PLUS[:stepsprorechnung+oldslice] = np.copy(u_ges_PLUS_read)
        dadt_ges_PLUS[:stepsprorechnung+oldslice] = np.copy(dadt_ges_PLUS_read)
        alpha_ges_PLUS[:stepsprorechnung+oldslice] = np.copy(alpha_ges_PLUS_read)

    print("Maximaler Alpha + 5°C: " + str(np.amax(alpha_ges_PLUS[slicer])) + " Minimaler Alpha: " + str(np.amin(alpha_ges_PLUS[slicer])))
 

    u_PLUS = u_ges_PLUS[slicer]   
    u_PLUS[0] = eingegeben + plus
    
    alpha_PLUS = alpha_ges_PLUS[slicer]
    dadt_PLUS = dadt_ges_PLUS[slicer]
    
    for i in range(slicer, stepsprorechnung+slicer):
       
        alpha0_PLUS = alpha_PLUS
        dadt0_PLUS = dadt_PLUS
        
        u0_PLUS = u_PLUS
        
        u_ges_PLUS, u0_PLUS, u_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, h_luft_ges_PLUS, alpha_PLUS, dadt_PLUS = timestep_lam(u0_PLUS, u_PLUS, u_ges_PLUS, u_left_PLUS, a_balsa, aa_balsa, k1, k2, 
            alpha_PLUS, alpha0_PLUS, dadt_PLUS, dadt0_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, reak_kinetic_ges_PLUS, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges_PLUS, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges_PLUS[i] = u_PLUS
        
        alpha_ges_PLUS[i] = alpha_PLUS
        dadt_ges_PLUS[i] = dadt_PLUS       
        
        if i == slicer:
            extracool_PLUS = np.copy(u_PLUS)
            
    u_ges_PLUS[slicer] = extracool_PLUS
    
    u_ges_PLUS_write = np.copy(u_ges_PLUS[:stepsprorechnung+slicer])
    dadt_ges_PLUS_write = np.copy(dadt_ges_PLUS[:stepsprorechnung+slicer])
    alpha_ges_PLUS_write = np.copy(alpha_ges_PLUS[:stepsprorechnung+slicer])

    if do_write:
        write.save_PLUS(u_ges_PLUS_write, alpha_ges_PLUS_write, dadt_ges_PLUS_write)

    
    result = np.where(u_ges_PLUS == np.amax(u_ges_PLUS[slicer:]))

    if np.isnan(plus):
        print("plus is NAN")
    else:
        print("wenn + "+str(round(plus,2))+ "°C: " + str(round(np.amax(u_ges_PLUS[slicer:])-273.15,2)) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
  
    return u_ges_PLUS, alpha_ges_PLUS, dadt_ges_PLUS, u_PLUS, u0_PLUS

def regelung2_MINUS(nsteps, dy, dt, dy2, ny, boundary1, boundary2, q, eingegeben,slicer, stepsprorechnung, oldslice, plus, **kwargs):
    if "write" in kwargs:
        do_write=kwargs["write"]
    else:
        do_write=True
   
    
    (u0_MINUS, u_MINUS, u_ges_MINUS, u_left_MINUS, a_balsa, aa_balsa, u0_MINUS, u_MINUS, u_ges_MINUS, k1, k2, 
     alpha_MINUS, alpha0_MINUS, dadt_MINUS, dadt0_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, 
     density_schicht, c_schicht, k_schicht
     , phi, density_M, h_luft_ges_MINUS) = setVal(ny, nsteps, dt, dy2) 
    
    u_ges_MINUS_read, alpha_ges_MINUS_read, dadt_ges_MINUS_read = write.read_MINUS()
    if "u_ges_MINUS" in kwargs:
        u_ges_MINUS_read=kwargs["u_ges_MINUS"]
    if "alpha_ges_MINUS" in kwargs:
        alpha_ges_MINUS_read=kwargs["alpha_ges_MINUS"]
    if "dadt_ges_MINUS" in kwargs:
        dadt_ges_MINUS_read=kwargs["dadt_ges_MINUS"]
   
    if q == 0:
        u_ges_MINUS[:stepsprorechnung] = np.copy(u_ges_MINUS_read)
        dadt_ges_MINUS[:stepsprorechnung] = np.copy(dadt_ges_MINUS_read)
        alpha_ges_MINUS[:stepsprorechnung] = np.copy(alpha_ges_MINUS_read)
    else:
        u_ges_MINUS[:stepsprorechnung+oldslice] = np.copy(u_ges_MINUS_read)
        dadt_ges_MINUS[:stepsprorechnung+oldslice] = np.copy(dadt_ges_MINUS_read)
        alpha_ges_MINUS[:stepsprorechnung+oldslice] = np.copy(alpha_ges_MINUS_read)
    
    print("Maximaler Alpha - 5°C: " + str(np.amax(alpha_ges_MINUS[slicer])) + " Minimaler Alpha: " + str(np.amin(alpha_ges_MINUS[slicer])))
 

    u_MINUS = u_ges_MINUS[slicer]   
    u_MINUS[0] = eingegeben - plus
    
    alpha_MINUS = alpha_ges_MINUS[slicer]
    dadt_MINUS = dadt_ges_MINUS[slicer]
    
    for i in range(slicer, stepsprorechnung+slicer):
       
        alpha0_MINUS = alpha_MINUS
        dadt0_MINUS = dadt_MINUS
        
        u0_MINUS = u_MINUS
        
        u_ges_MINUS, u0_MINUS, u_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, h_luft_ges_MINUS, alpha_MINUS, dadt_MINUS = timestep_lam(u0_MINUS, u_MINUS, u_ges_MINUS, u_left_MINUS, a_balsa, aa_balsa, k1, k2, 
            alpha_MINUS, alpha0_MINUS, dadt_MINUS, dadt0_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, reak_kinetic_ges_MINUS, 
            density_schicht, c_schicht, k_schicht, phi, 
            density_M, h_luft_ges_MINUS, nsteps, dy, dt, dy2, ny, boundary1, boundary2)
      
        u_ges_MINUS[i] = u_MINUS
        
        alpha_ges_MINUS[i] = alpha_MINUS
        dadt_ges_MINUS[i] = dadt_MINUS       
        
        if i == slicer:
            extracool_MINUS = np.copy(u_MINUS)
            
    u_ges_MINUS[slicer] = extracool_MINUS
    
    u_ges_MINUS_write = np.copy(u_ges_MINUS[:stepsprorechnung+slicer])
    dadt_ges_MINUS_write = np.copy(dadt_ges_MINUS[:stepsprorechnung+slicer])
    alpha_ges_MINUS_write = np.copy(alpha_ges_MINUS[:stepsprorechnung+slicer]) 
    if do_write:
        write.save_MINUS(u_ges_MINUS_write, alpha_ges_MINUS_write, dadt_ges_MINUS_write)

    result = np.where(u_ges_MINUS == np.amax(u_ges_MINUS[slicer:]))

    print("wenn - "+str(round(plus,2))+ "°C: "  + str(round(np.amax(u_ges_MINUS[slicer:])-273.15,2)) + " °C nach " + str(result[0]) + " Sekunden, bei " + str(result[1]) + " mm.")
  
    return u_ges_MINUS, alpha_ges_MINUS, dadt_ges_MINUS, u_MINUS, u0_MINUS