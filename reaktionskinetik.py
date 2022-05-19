"""
Hier werden alle Vorbereitungen und Methoden für die Reaktionskinetik initialisiert
"""
import numpy as np
import materialparameter

def reakParameter():
    
    A1 = 200000
    E1 = 63267.9637
    A2 = 118000.438
    E2 = 55157.8279
    s = 0.30450112
    v = 1.61742134
    R = 8.314
    Htot = 450 * 1000 #450 * 1000 
    alpha_start = 0.0000001 #0.00000001
    heizrate = 2.5  #pro sekunde
    
    return A1, E1, A2, E2, s, v, R, Htot, alpha_start, heizrate

def reakParameter_135():
    
    A1 = 35982
    E1 = 54960
    A2 = 3574.1
    E2 = 44289
    s = 0.39845
    v = 1.5361
    R = 8.314
    Htot = 460 * 1000 #450 * 1000 
    alpha_start = 0.0000001 #0.00000001
    Ad = 7*10**18
    Ed = 137300
    alphaf = 0.00048
    b = 0.009
    fg = 0.025
    Tg0 = -57
    Tg00 = 91
    Lambda = 0.36903
    heizrate = 2.5  #pro sekunde
    
    return A1, E1, A2, E2, s, v, R, Htot, alpha_start, heizrate, Ad, Ed, alphaf, b, fg, Tg0, Tg00, Lambda

def reakArrays(ny, nsteps):
    
    A1, E1, A2, E2, s, v, R, Htot, alpha_start, heizrate = reakParameter()
    k1 = np.zeros(ny)
    k2 = np.zeros(ny)
    alpha = np.ones(ny) * alpha_start
    alpha0 = alpha_start * np.ones(ny)
    dadt = np.zeros(ny) 
    dadt0 = dadt.copy()
    alpha_ges = np.ones((nsteps, ny))
    dadt_ges = np.copy(alpha_ges)
    reak_kinetic_ges = np.copy(alpha_ges)
    
    return k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges

def calcReaktionskinetik(ny, dt,  phi, density_M, density_schicht, u0, u, boundary1, boundary2, nsteps, alpha0, dadt0):
    
    A1, E1, A2, E2, s, v, R, Htot, alpha_start, heizrate = reakParameter()
    #k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges = reakArrays(ny, nsteps)
    
    k1 = A1 * np.exp(-E1/(R*u0))
    k2 = A2 * np.exp(-E2/(R*u0))
    alpha = alpha0 + (dadt0*dt)    
    dadt = ((k1 + (k2 * (alpha)**s))) * (1 - alpha)**v
    cp_comp = materialparameter.calc_cp_epoxy(u, alpha, ny)
    
    reak_kinetik = dt * ((dadt * Htot * (1 - phi) * density_M) / (cp_comp * density_schicht))
    
    #hier herrausfinden wie genau boundary1 und boundary 2 funktionieren.
    return reak_kinetik, alpha, dadt

def calcReaktionskinetik_135(ny, dt,  phi, density_M, density_schicht, u0, u, boundary1, boundary2, nsteps, alpha0, dadt0):
    
    A1, E1, A2, E2, s, v, R, Htot, alpha_start, heizrate, Ad, Ed, alphaf, b, fg, Tg0, Tg00, Lambda = reakParameter_135()
    #k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges = reakArrays(ny, nsteps)
    
    alpha = alpha0 + (dadt0*dt) 
    kc1 = A1 * np.exp(-E1/(R*u0))
    kc2 = A2 * np.exp(-E2/(R*u0))
    Tg = Tg0 + ((Tg00-Tg0) * Lambda * alpha)/(1-(1-Lambda)*alpha) +273.15
    kd = Ad  * np.exp(-Ed/(R*u0))* np.exp(-b/(alphaf * (u0-Tg)+fg))
    k1 = 1/((1/kc1)+(1/kd))
    k2 = 1/((1/kc2)+(1/kd))
     
    dadt = ((k1 + (k2 * (alpha)**s))) * (1 - alpha)**v
    cp_comp = materialparameter.calc_cp_epoxy(u, alpha, ny)
    
    reak_kinetik = dt * ((dadt * Htot * (1 - phi) * density_M) / (cp_comp * density_schicht))
    
    #hier herrausfinden wie genau boundary1 und boundary 2 funktionieren.
    return reak_kinetik, alpha, dadt, Tg