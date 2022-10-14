"""
functions used for heat conduction computations
"""
import numpy as np
import materialparameter as m

# temperature of environment ("air")
#T_out = 25.2 # 23.1 #None         -> moved to reg.py
# starting temperature for temperature arrays
u_init = 39 #None #39 #23
# starting boundary condition for temperature arrays
u_left = 41 # anywayNone #41 #never really used?? is overwritten in reg.py regelung1, regelung2,... (eingeben1 and eingegeben, i.e entered/measured value)
#h_luft_covered = None #4

def set_layer_composition(core): # set core
    # set it in m:
    m.density_core, m.c_core, m.k_core = m.materialParam(core)

#Initiate Arrays, starting temperatur and starting BC for the temperature arrays
def uArrays(ny, nsteps):
    global u_init, u_left
    u0 = u_init * np.ones(ny)
    u0[0] = u_left
    u = u0.copy()
    u_ges = np.ones((nsteps, ny))
    
    return u0, u, u_ges, u_left

#Convert celcius to kelvin and vice versa
def celius_to_kelvin(*args):
    return tuple(num+273.15 for num in args)
    
def kelvin_to_celsius(*args):
    return tuple(num-273.15 for num in args)

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
    #print("calcU leftb: "+str(leftB)+" rightb: "+str(rightB))
    #print("calcU u0: "+str(u0))
    #print("calcU a[leftB:rightB]: "+str(a[leftB:rightB]))
    #print("calcU: prod"+str((u0[leftB+1:] - 2*u0[leftB:rightB] + u0[leftB-1:rightB-1])))
    u[leftB:rightB] = u0[leftB:rightB] + a[leftB:rightB] * (u0[leftB+1:] - 2*u0[leftB:rightB] + u0[leftB-1:rightB-1])  ##### !!!!!!!!!!!!!!!!u0[leftB+1:]  Fehler???????????
    return u

"""
interfaceBoundary 1 and 2 are previously mentioned calculations for the boundaries
"""

def interfaceBoundary1(aa_schicht, aa_balsa, u0, boundary1):
    
    #WICHTIG: Beachten in welcher Richtung Temperaturfluss --> Diffusivitätsquotient
    
    l1 = 1/(aa_schicht[boundary1]/aa_balsa)
    #print("l1:"+str(l1))
    
    u0[boundary1] = ((l1 * u0[boundary1+1]) +u0[boundary1-2]) / (1+l1)
    #print("u0[boundary1]:"+str(u0[boundary1]))
    return u0[boundary1]

def interfaceBoundary2(aa_schicht, aa_balsa, u0, boundary2):
    
    l2 = (aa_schicht[boundary2]/aa_balsa)
    #print("l2:"+str(l2))
    
    u0[boundary2] = ((l2 * u0[boundary2+1]) +u0[boundary2-2]) / (1+l2)
    #print("u0[boundary2]:"+str(u0[boundary2]))
    return u0[boundary2]

#The outermost boundary is a robin boundary, which is a boundary that approximates
#a heat dissipation in air

def robinBoundary(ny, k_comp, dy, u, u0, density_schicht, cp_comp, **kwargs):
    global h_luft_covered
    if "h_luft_covered" in kwargs:
        h_luft_covered=kwargs["h_luft_covered"]
    #else:
    #    h_luft_covered = h_luft_covered
    
    if "switchH" in kwargs:
        switchH=kwargs["switchH"]
    else:
        switchH = False

    if "T_out" in kwargs:
        T_out=kwargs["T_out"]
    else:
        T_out = 23.0
    
    #global T_out #T_out = 25.2 # 23
    #The switch controls wether the heat dissipation coefficient gets calculated or is a 
    #fixed value. Switch can be turned on and off while the main program loop is running
    #print("switch: "+str(switchH))
    if switchH == False:
        h_luft = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out, QuadSize = 1/480) #*2 #for testing purposes
        #h_luft2 = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out, k_air = 0.0245) 
        #h_luft3 = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out, QuadSize = 1/120) 
        #h_luft4 = m.hSchicht(density_schicht, cp_comp, k_comp, u, T_out, QuadSize = 1/240) 
        #print("khluft: ",h_luft,"khluft2: ",h_luft2,"khluft3: ",h_luft3,"khluft4: ",h_luft4)
        #khluft:  16.659653654584876 k_air = 0.0245:  17.530979713138457 QuadSize = 1/60:  14.009043037508867 QuadSize = 1/240:  19.811778659513422
    if switchH == True:
        h_luft = h_luft_covered
        #print("ein Vlies!")
        
    #print(switchH)
    #print((dy,h_luft,T_out, k_comp[-1]))
    Z1 = ((dy*h_luft*(T_out + 273.15)))/((dy*h_luft)+k_comp[-1])
    B = k_comp[-1]/((dy*h_luft)+k_comp[-1])
    #print('robin')
    #print((B, Z1, u0[-2]), k_comp, dy, h_luft)
    T_grenze = Z1+B*u0[-2]
    
    u[-1] = T_grenze 
    #print(T_grenze- 273.15)
    return u, h_luft

