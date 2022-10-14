"""
Definitions of material parameters
"""
import numpy as np
import pandas as pd
    
# material parameters
# not to be used inside simulation loops, because it is slow
def materialParam(material):
    material_data = [['epoxy', 1150, 1400, 0.2], # material, density, c, k   #Diffusivity relevant for heat equation parameter for epoxy without temperature dependence
                    ['epoxy_cured', 1150, 1100, 0.10],
                    ['epoxy_uncured', 1150, 1642.1, 0.15],
                    ['AirrexC70', 80, 1200, 0.041],  # 40-250 (TDS), estimated, 0.031-0.056 (TDS)   #keine Temperaturabhängigkeit
                    ['glassfibre', 2600, 807, 1],  # phi = 0.55 #Faservolumengehalt not in db?
                    ['balsa', 140, 2720, 0.06]]  # k_balsa in 0.06-0.0935 #############################################
    material_data = pd.DataFrame(material_data, columns=['material', 'density', 'c', 'k'])
    material_data = material_data.set_index('material')
    
    try:
        return material_data.loc[material]
    except:
        raise('unknown material: '+str(material))
        
# save often used material parameters as global variable
phi = bf_fvc = None #0.57 #0.55 # fiber volume content of glass fibres
density_M, c_M, k_M = materialParam('epoxy')
_,_,k_harz_cured    = materialParam('epoxy_cured')
_,_,k_harz_uncured  = materialParam('epoxy_uncured')
density_F, c_F, k_F = materialParam('glassfibre')
density_core, c_core, k_core = float("nan"), float("nan"), float("nan") #density_core, c_core, k_core = materialParam('balsa')

#Calculated a GFRP laminate based on the parameters given above, with no temperature dependency
def calcVerbund(**kwargs): # should this really be a function? Isn't this returning constant values?
    global density_M, c_M, k_M, phi, density_F, c_F, k_F
    
    if "phi" in kwargs:
        phi=kwargs["phi"]
    #else:
    #    phi = phi
    
    density_schicht = phi * density_F + (1 - phi) * density_M
    c_schicht = (phi * density_F * c_F + (1-phi) * density_M * c_M) / (phi 
                                            *density_F + (1-phi) * density_M)
    k_schicht = k_M * ((k_F * (1+phi)+k_M*(1-phi))/(k_F * (1-phi)+k_M*(1-phi)))
    
    return density_schicht, c_schicht, k_schicht, phi, density_M

#Heat equation requires the diffusivity of a material which gets calculated here:
def calcDiffusivityBalsa(dt, dy2):
    global density_core, c_core, k_core
    
    a_core = k_core/(density_core * c_core) 
    aa_core = (a_core * dt)/dy2
    
    return a_core, aa_core 


#The follwing functions calculate cp, and k of epoxy resin temperature dependant
def calc_cp_epoxy(u, alpha, ny, **kwargs):
    global phi, density_M, density_F, c_F #, c_M, k_M, k_F
    
    if "phi" in kwargs:
        phi=kwargs["phi"]
    #else:
    #    phi = phi
     
    cp_epoxycured = np.ones(ny)
    cp_epoxyuncured = np.ones(ny)
    
    #Temperature dependency:
    cp_epoxycured = 4.608 * u + 1100  
    cp_epoxyuncured = 1.6 * u + 1642.1
    #Dependency on degree of cure:
    cp_harz = np.ones(ny)
    cp_harz = alpha*cp_epoxycured + (1 - alpha)*cp_epoxyuncured

    cp_comp = np.ones(ny)
    cp_comp = (phi*density_F * 
       c_F + (1 - phi)*density_M*cp_harz)/(phi*density_F + (1 - phi)*density_M)
       
    if (cp_comp<0).any():
        raise ValueError("cp_comp < 0 in calc_cp_epoxy:"+str(cp_comp)+"phi="+str(phi)+"density_M="+str(density_M)+"cp_harz="+str(cp_harz)+"density_F="+str(density_F)+"c_F="+str(c_F))
    
    return cp_comp

def calc_k_epoxy(alpha, ny, **kwargs):
    global phi, density_F, c_F, k_F, k_harz_cured, k_harz_uncured
        
    if "phi" in kwargs:
        phi=kwargs["phi"]
    #else:
    #    phi = phi
    
    #k_harz_cured = 0.10#0.15
    #k_harz_uncured = 0.15# 0.23
    k_harz = np.ones(ny)
    k_harz = alpha*k_harz_cured + (1 - alpha)*k_harz_uncured
    
    k_comp = np.ones(ny)
    
    #k_comp = k_harz*(1 - phi) + k_F*phi

    k_comp = k_harz * ((k_F * (1+phi)+k_harz*(1-phi))/(k_F * (1-phi)+k_harz*(1-phi)))

    return k_comp
    
#Calculates the GFRP Laminate with temperature and Degree of curing dependency:
def calcSchichtT(ny, alpha, u, dt, dy2, **kwargs):

    if "phi" in kwargs:
        phi=kwargs["phi"]
    #else:
    #    phi = phi
    
    density_schicht, _, _, _, _ = calcVerbund(phi=phi)
    k_comp = calc_k_epoxy(alpha, ny, phi=phi)
    cp_comp = calc_cp_epoxy(u, alpha, ny, phi=phi)
    #print("cpcomp:"+str(cp_comp)+" phi: "+str(phi))
    a_schicht = np.ones(ny) #unnecessary?
    a_schicht = k_comp/(density_schicht * cp_comp) #####   ((kg m²/s³)/(m*K))/((kg/m3) * ((kg m²/s²)/(K*kg)) ) = m^2/s
    
    aa_schicht = np.ones(ny) #unnecessary?
    aa_schicht = (a_schicht * dt)/dy2   ####  = (m^2/s) * s / m² = scalar
    
    return a_schicht, aa_schicht, density_schicht, k_comp, cp_comp

#Calculation of the heat transfer coefficient of the air at the upper boundary:
def hSchicht(density_schicht, cp_comp, k_comp, u, Text, **kwargs):  
    # cp_comp: specific heat (vector with values through thickness)
    # cp_comp[-1]: specific heat at the top
    
    # thermal conductivity of air at 30° [kcal(IT)/(h m K)]: 0.02289
    if "k_air" in kwargs:
        k_air=kwargs["k_air"]
    else:
        k_air = 0.02289 #[kcal(IT)/(h m K)]
        
    if "QuadSize" in kwargs:
        QuadSize=kwargs["QuadSize"]
    else:
        QuadSize = 1/120 # Elementsize from which heat is transferred. Has to be calibrated by hand
    
    g = 9.81         # gravitational acceleration due to Earth
    # dynamic viscosity (μ) ## acc to some ressources: 
	# µ = 	1.825 x 10	, kg/m*s    at 20°C and 200 kPa is 1.83 × 10–5 kg/m·s.
    #dynamic_viscosity = 0.0000182
    #dynamic_viscosity = (2*10**-7)*(u[-1]-273.15)+2*10**-5  # which formula is that???
    # dynamic viscosity of air due to wikipedia: tec-science (2020-03-25). "Viscosity of liquids and gases". tec-science.
    dynamic_viscosity = dyn_viscosity = 2.791 * 10**(-7) * u[-1]**0.7355  # dynamic viscosity is pressure dependent for high pressures... is this formula ok in thes case?
    #print("dynamic viscosity (?0.0000182): "+str(dynamic_viscosity) + ", or: " + str(dyn_viscosity))
    # density of air at 35°C
    density_air = 1.1455  
    # kinematic_viscosity
    kinematic_viscosity= dynamic_viscosity/density_air 
    # coefficient of thermal expansion (equal to approximately 1/T, for ideal gases)
    ap = 1/Text  
    # Prandtl Number
    Pr = (dynamic_viscosity * cp_comp[-1])/ k_air
    # Grashof Number     
    if ((u[-1]-273.15) - Text)<-0.2:
        import warnings
        warnings.warn("warning: GrL="+str((g * ap * ((u[-1]-273.15) - Text) * QuadSize**3)/kinematic_viscosity**2)+", u[-1]-273.15="+str(u[-1]-273.15)+", T_ext="+str(Text))
    GrL = (g * ap * max(0, (u[-1]-273.15) - Text) * QuadSize**3)/ kinematic_viscosity**2 
    # Rayleigh number = Grashof number * Prandtl number
    RaL = GrL * Pr 
    
    #h_luft = (k_comp[-1]/L) * 0.27 * RaL**(1/4)
    try:
        #print("RaL/GrL/Pr/Text/ap/dynamic_viscosity/u[-1]:"+str(RaL,GrL, Pr, Text,ap,dynamic_viscosity,u[-1]))            
        if np.isnan(RaL**(1/4)):
            raise("RaL**(1/4) is nan")
            
        #print("thermal conductivity of air near 0.02289?:" + str(k_comp[-1])) # about 0.46615094330309775
        # Heat transfer coefficient; external flow, horizontal plates, 
        # For a hot surface facing down, or a cold surface facing up, for laminar flow:
        # [McAdams, William H. (1954). Heat Transmission (Third ed.). New York: McGraw-Hill. p. 180.]
        #h_luft = (k_air/QuadSize) * 0.27 * RaL**(1/4)  # ist das nicht verkehrt??? Bei Rand zur Luft ist die kältere Fläche oben, also face down
        # formula for a hot surface facing up, or a cold surface facing down, for laminar flow:
        h_luft = (k_air/QuadSize) * 0.54 * RaL**(1/4) 
    except: # IndexError:
        print("Error in hSchicht; h_luft: QuadSize="+str(QuadSize)+", RaL="+str(RaL)+", ap="+str(ap)+",Pr="+str(Pr)+",GrL:"+str(GrL)+",dynamic_viscosity="+str(dynamic_viscosity)+",cp_comp[-1]="+str(cp_comp[-1])+"k_air="+str(k_air))
        #print("RaL**(1/4)"+str(RaL**(1/4)))
        raise ValueError("stopped")
       
    #print("hluft:"+str(h_luft)) # meistens < 7....
    #h_luft = 20
    return h_luft
