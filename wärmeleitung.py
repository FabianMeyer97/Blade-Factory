"""
Hier werden Arrays und Berechnungen für die Wärmeleitung definiert
"""
import numpy as np
import materialparameter as m

switchH = False

def uArrays(ny, nsteps):
    
    u_init = 23
    u_left = 40
    u0 = u_init * np.ones(ny)
    u0[0] = u_left
    u = u0.copy()
    u_ges = np.ones((nsteps, ny))
    
    return u0, u, u_ges, u_left
    
def celius_to_kelvin(u0, u, u_ges):
    
    u0 += 273.15
    u += 273.15
    u_ges += 273.15
    
    return u0, u, u_ges

def kelvin_to_celsius(u0, u, u_ges):
    
    u0 -= 273.15
    u -= 273.15
    u_ges -= 273.15
    
    return u0, u, u_ges

def calcU1(u, u0, a, leftB, rightB):
    
    u[leftB:rightB-1] = u0[leftB:rightB-1] + a[leftB:rightB-1] * (u0[leftB+1:rightB] - 2*u0[leftB:rightB-1] + u0[leftB-1:rightB-2])

    return u

def calcU2(u, u0, a, leftB, rightB):
    
    u[leftB:rightB-1] = u0[leftB:rightB-1] + a * (u0[leftB+1:rightB] - 2*u0[leftB:rightB-1] + u0[leftB-1:rightB-2])

    return u

def calcU3(u, u0, a, leftB, rightB):
    
    u[leftB:-1] = u0[leftB:-1] + a[leftB:-1] * (u0[leftB+1:] - 2*u0[leftB:-1] + u0[leftB-1:-2])

    return u

def calcU(u, u0, a, leftB, rightB):
    
    u[leftB:rightB] = u0[leftB:rightB] + a[leftB:rightB] * (u0[leftB+1:] - 2*u0[leftB:rightB] + u0[leftB-1:rightB-1])

    return u

def interfaceBoundary1(aa_schicht, aa_balsa, u0, boundary1):
    
    #WICHTIG: Beachten in welcher Richtung Temperaturfluss --> Diffusivitätsquotient
    
    l1 = 1/(aa_schicht[boundary1]/aa_balsa)
    
    u0[boundary1] = ((l1 * u0[boundary1+1]) +u0[boundary1-2]) / (1+l1)
    
    return u0[boundary1]

def interfaceBoundary2(aa_schicht, aa_balsa, u0, boundary2):
    
    l2 = (aa_schicht[boundary2]/aa_balsa)
    
    u0[boundary2] = ((l2 * u0[boundary2+1]) +u0[boundary2-2]) / (1+l2)
    
    return u0[boundary2]

def robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp):
    
    T_out = 23
    if switchH == False:
        h_luft = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out)
    if switchH == True:
        h_luft = 1
    Z1 = ((dy*h_luft*(T_out + 273.15)))/((dy*h_luft)+k_comp[-1])
    B = k_comp[-1]/((dy*h_luft)+k_comp[-1])
    T_grenze = Z1+B*u0[-2]
    
    u[-1] = T_grenze
    
    return u, h_luft

