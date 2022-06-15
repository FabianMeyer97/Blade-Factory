"""
Definitions of material parameters
"""
import numpy as np


#parameter for epoxy without temperature dependence:
def parameterMatrix():   #Parameter von Epoxy Resin
    density_M = 1150
    c_M = 1400
    k_M = 0.2  
    return density_M, c_M, k_M

#Paramter AirrexC70:
def parameterAirrexC70(): #keine Temperaturabhängigkeit
    
    density_A = 40-250 #RANGE LAUT DATENBLATT
    c_A= 1200 #SCHÄTZWERT
    k_A = 0.031-0.056 #RANGE LAUT DATENBLATT
    
    return density_A, c_A, k_A

#Parameter for glas fibre:    
def parameterFaser(): 
    phi = 0.55 #Faservolumengehalt
    density_F = 2600
    c_F = 807
    k_F = 1   
    return phi, density_F, c_F, k_F

#Calculation of the heat transfer coefficient of the air at the upper boundary:
def hSchicht(density_schicht, cp_comp, k_comp, u, Text):  
    g = 9.81
    QuadSize = 1/120 #Elementsize from which heat is transferred. Has to be calibrated by hand
    
    #dynamic_viscosity = 0.0000182
    dynamic_viscosity = (2*10**-7)*(u[-1]-273.15)+2*10**-5
    ap = 1/Text
    Pr = (dynamic_viscosity * cp_comp[-1])/ 0.02289 #Prandtl Number
    GrL = (g * ap * ((u[-1]-273.15) - Text) * QuadSize**3)/ (dynamic_viscosity / 1.1455)**2 #Grashof Number 
    
    RaL = GrL * Pr #Rayleigh number 
    #h_luft = (k_comp[-1]/L) * 0.27 * RaL**(1/4)
    h_luft = (0.02289/QuadSize) * 0.27 * RaL**(1/4)  #heat transfer coefficient 
    #h_luft = 20
    return h_luft

#Parameter for Balsa Wood
def parameterBalsa():  
    k_balsa = 0.06 #0.06-0.0935
    density_balsa = 140
    c_balsa = 2720   
    return k_balsa, density_balsa, c_balsa

#Calculated a GFRP laminate based on the parameters given above, with no temperature dependency
def calcVerbund():
    
    density_M, c_M, k_M = parameterMatrix()
    phi, density_F, c_F, k_F = parameterFaser()
    
    density_schicht = phi * density_F + (1 - phi) * density_M
    c_schicht = (phi * density_F * c_F + (1-phi) * density_M * c_M) / (phi 
                                            *density_F + (1-phi) * density_M)
    k_schicht = k_M * ((k_F * (1+phi)+k_M*(1-phi))/(k_F * (1-phi)+k_M*(1-phi)))
    
    return density_schicht, c_schicht, k_schicht, phi, density_M

#Heat equation requires the diffusivity of a material which gets calculated here:
def calcDiffusivityBalsa(dt, dy2):
    
    k_balsa, density_balsa, c_balsa = parameterBalsa()
    a_balsa = k_balsa/(density_balsa * c_balsa) 
    aa_balsa = (a_balsa * dt)/dy2
    
    return a_balsa, aa_balsa


#The follwing functions calculate cp, and k of epoxy resin temperature dependant
def calc_cp_epoxy(u, alpha, ny):
    
    
    cp_epoxycured = np.ones(ny)
    cp_epoxyuncured = np.ones(ny)
    
    #Temperature dependency:
    cp_epoxycured = 4.608 * u + 1100  
    cp_epoxyuncured = 1.6 * u + 1642.1
    #Dependency on degree of cure:
    cp_harz = np.ones(ny)
    cp_harz = alpha*cp_epoxycured + (1 - alpha)*cp_epoxyuncured
    
    density_M, c_M, k_M = parameterMatrix()
    phi, density_F, c_F, k_F = parameterFaser()

    cp_comp = np.ones(ny)
    cp_comp = (phi*density_F * 
       c_F + (1 - phi)*density_M*cp_harz)/(phi*density_F + (1 - phi)*density_M)
    
    return cp_comp

def calc_k_epoxy(alpha, ny):
    
    k_harz_cured = 0.10#0.15
    
    k_harz_uncured = 0.15# 0.23
    
    k_harz = np.ones(ny)
    
    k_harz = alpha*k_harz_cured + (1 - alpha)*k_harz_uncured
    
    phi, density_F, c_F, k_F = parameterFaser()
    
    k_comp = np.ones(ny)
    
    #k_comp = k_harz*(1 - phi) + k_F*phi

    k_comp = k_harz * ((k_F * (1+phi)+k_harz*(1-phi))/(k_F * (1-phi)+k_harz*(1-phi)))

    return k_comp
#Calculates the GFRP Laminate with temperature and Degree of curing dependency:
def calcSchichtT(ny, alpha, u, dt, dy2):
    
    density_schicht, c_schicht, k_schicht, phi, density_M = calcVerbund()
    k_comp = calc_k_epoxy(alpha, ny)
    cp_comp = calc_cp_epoxy(u, alpha, ny)
    a_schicht = np.ones(ny)
    a_schicht = k_comp/(density_schicht * cp_comp) #mm^2/s
    
    aa_schicht = np.ones(ny)
    aa_schicht = (a_schicht * dt)/dy2
    
    return a_schicht, aa_schicht, density_schicht, k_comp, cp_comp

#TODO: Bessere Einbindung verschiedener Matrix und Kernstoffe.
        #Bibliothek?