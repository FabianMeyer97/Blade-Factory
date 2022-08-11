"""
Hier werden Arrays und Berechnungen für die Wärmeleitung definiert
"""
import numpy as np
import materialparameter as m

#switchH acts as a "lever"; while False, the Heattransfer coefficiant is calculated
#if it's True the HTC is adjusted to match a "fleece" on the object
switchH = False

# temperature of environment ("air")
T_out = 23.1 #None
# starting temperature for temperature arrays
u_init = 39 #None #39
# starting boundary condition for temperature arrays
u_left = None #41 #never really used?? is overwritten in reg.py regelung1, regelung2,... (eingeben1 and eingegeben, i.e entered/measured value)

#Initiate Arrays, starting temperatur and starting BC for the temperature arrays
def uArrays(ny, nsteps):
    global u_init, u_left
    #u_init = 39 #23
    #u_left = 41
    u0 = u_init * np.ones(ny)
    u0[0] = u_left
    u = u0.copy()
    u_ges = np.ones((nsteps, ny))
    
    return u0, u, u_ges, u_left

#Convert celcius to kelvin and vice versa
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
"""
If you want to calculate the heat transfer over different materials the heat eqution needs
to be broken up upon the various materials. A sandwich GFRP-component needs 3 different heat
equations. To "connect" the seperate equations, the adjacent points share a boundary condition.
This interface boundary conditions calculates the temperature at the boundary dependent on
the material parameters. 
"""

#Calc U1-3 are the broken up heat equations for a sandwich component.
def calcU1(u, u0, a, leftB, rightB): 
    u[leftB:rightB-1] = u0[leftB:rightB-1] + a[leftB:rightB-1] * (u0[leftB+1:rightB] - 2*u0[leftB:rightB-1] + u0[leftB-1:rightB-2])
    return u

def calcU2(u, u0, a, leftB, rightB): 
    u[leftB:rightB-1] = u0[leftB:rightB-1] + a * (u0[leftB+1:rightB] - 2*u0[leftB:rightB-1] + u0[leftB-1:rightB-2])
    return u

def calcU3(u, u0, a, leftB, rightB):
    u[leftB:-1] = u0[leftB:-1] + a[leftB:-1] * (u0[leftB+1:] - 2*u0[leftB:-1] + u0[leftB-1:-2])
    return u

#CalcU calculates a complete component without being broken up
def calcU(u, u0, a, leftB, rightB): 
    u[leftB:rightB] = u0[leftB:rightB] + a[leftB:rightB] * (u0[leftB+1:] - 2*u0[leftB:rightB] + u0[leftB-1:rightB-1])
    return u

"""
interfaceBoundary 1 and 2 are previously mentioned calculations for the boundaries
"""

def interfaceBoundary1(aa_schicht, aa_balsa, u0, boundary1):
    
    #WICHTIG: Beachten in welcher Richtung Temperaturfluss --> Diffusivitätsquotient
    
    l1 = 1/(aa_schicht[boundary1]/aa_balsa)
    
    u0[boundary1] = ((l1 * u0[boundary1+1]) +u0[boundary1-2]) / (1+l1)
    
    return u0[boundary1]

def interfaceBoundary2(aa_schicht, aa_balsa, u0, boundary2):
    
    l2 = (aa_schicht[boundary2]/aa_balsa)
    
    u0[boundary2] = ((l2 * u0[boundary2+1]) +u0[boundary2-2]) / (1+l2)
    
    return u0[boundary2]

#The outermost boundary is a robin boundary, which is a boundary that approximates
#a heat dissipation in air

def robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp):
    global T_out #T_out = 25.2 # 23
    #The switch controls wether the heat dissipation coefficient gets calculated or is a 
    #fixed value. Switch can be turned on and off while the main program loop is running
    if switchH == False:
        h_luft = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out)
    if switchH == True:
        h_luft = 1
    Z1 = ((dy*h_luft*(T_out + 273.15)))/((dy*h_luft)+k_comp[-1])
    B = k_comp[-1]/((dy*h_luft)+k_comp[-1])
    T_grenze = Z1+B*u0[-2]
    
    u[-1] = T_grenze 
    return u, h_luft

