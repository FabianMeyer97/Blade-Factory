"""
Initialization and methods to calculate reaction kinetics
Atm a function to solve the regular Kamal-Souror and advanced Kamal-Souror with flow control are implemented
To add a new modell, copy the existing functions for parameters and calculations and adjust accordingly
"""
import numpy as np
#import materialparameter
from materialparameter import calc_cp_epoxy   #independent of layer composition, for fixed epoxy and glass fiber no initialisation for "materialparameter" is necessary

advancedKS = True
# false for regular Kamal-Souror,
# true for advanced Kamal-Souror
resinSystem = 135  
#  135 for RIMR135-RIMH137 
#   35 for RIMR035c-RIMH037
# 1037 for RIMR1037-RIMH1037
alpha_start = None # 0.04 #0.0000001 #0.00000001
R = 8.31446261815324  # molar gas constant (kg m²)/(s² mol K)
advancedKS = False
resinSystem = 35  

#def set_layer_composition(core): # set core
#    # set the layer composition in materialparameter:
#    materialparameter.density_core, materialparameter.c_core, materialparameter.k_core = materialparameter.materialParam(core)

#Function returns the parameters needed for the regular Kamal-Souror approximations:
def reakParameter_35(): #035  
    # Daten aus: \\fib-19-file\projekte\Projekt-Aktuell\MS_BladeFactory2025\7 Projektinhalt\AP 3.4.1 Eingungsuntersuchung\03_Kinetik\035c\Kinetik_035c_210917.xlsx
    # Worksheet: Fitting_Python
    A1 = 200000           # Arrhenius: pre-factor in 1/s
    E1 = 63267.9637       # Arrhenius: activation energy in J/mol
    A2 = 118000.438       # Arrhenius: pre-factor in 1/s
    E2 = 55157.8279       # Arrhenius: activation energy in J/mol
    s = 0.30450112        # reaction order m for Kamal-Souror
    v = 1.61742134        # reaction order n for Kamal-Souror
    Htot = 450 * 1000     # Total Enthalpy H_tot in J/kg           #446+-10  # Quelle?
    R = None
    heizrate = None #2.5  #pro sekunde 
    Tg0 = -10 #guess        # Tg of the uncured resin  # https://www.hexion.com/CustomServices/PDFDownloader.aspx?type=tds&pid=bf1dc63d-5814-6fe3-ae8a-ff0300fcd525
    Tg00 = 87 #guess        # Tg_infty, # https://www.hexion.com/CustomServices/PDFDownloader.aspx?type=tds&pid=bf1dc63d-5814-6fe3-ae8a-ff0300fcd525
    return A1, E1, A2, E2, s, v, R, Htot, None, heizrate, Tg0, Tg00

#Parameters for the advanced Kamal-Souror approximation:
def reakParameter_135(): 
    # sources:
    # [*] https://doi.org/10.1016/j.tca.2015.11.014
    A1 = 35982           # Arrhenius: pre-factor        [1/s]   (kinetically-controlled reaction)  # [*] Table 5
    E1 = 54960           # Arrhenius: activation energy [J/mol] (kinetically-controlled reaction)  # [*] Table 5
    A2 = 3574.1          # Arrhenius: pre-factor        [1/s]   (kinetically-controlled reaction)  # [*] Table 5
    E2 = 44289           # Arrhenius: activation energy [J/mol] (kinetically-controlled reaction)  # [*] Table 5
    Ad = 7*10**18        # Arrhenius: pre-factor        [1/s]   (diffusion)                        # [*] Table 5
    Ed = 137300          # Arrhenius: activation energy [J/mol] (diffusion)                        # [*] Table 5
    s = 0.39845          # Kamal-Souror: reaction order m                                          # [*] Table 5
    v = 1.5361           # Kamal-Souror: reaction order n                                          # [*] Table 5
    Lambda = 0.36903     # DiBenedetto: fitting parameter (changes in heat capacity at Tg)         # [*] Table 5
    b = 0.009            # Huguenin: fitting parameter / material constant                         # [*] Table 5
    alphaf = 0.00048     # Huguenin: Lin. Ausdehnungskoeffizient des freien Volumens [1/K]         # [*] eq. 7
    fg = 0.025           # Huguenin : Freies Volumen zur Glasübergangstemperatur f_g               # [*] eq. 7
    Htot = 460*1000      # total heat of the reaction (fiting parameter), Htot in J/g  #450 * 1000 # cf: 446 in [*] 4.1
    Tg0 = -57            # Tg of the uncured resin                                        [°C]     # [*] 4.) 
    Tg00 = 91            # Tg_infty, maximum obtainable glass transition temperaturedetto [°C]     # [*] 4.) 
    heizrate = None #2.5  #pro sekunde
    R = None
    
    return A1, E1, A2, E2, s, v, R, Htot, None, heizrate, Ad, Ed, alphaf, b, fg, Tg0, Tg00, Lambda

#Function initializes the arrays needed to run the calculations
def reakArrays(ny, nsteps, **kwargs): 
    global alpha_start

    if "alpha_start" in kwargs:
        alpha_start=kwargs["alpha_start"]
    #else:
    #    alpha_start = alpha_start
    
    if "dt" in kwargs:
        dt=float(kwargs["dt"])
    else:
        dt=1
    
    k1 = np.zeros(ny)
    k2 = np.zeros(ny)
    alpha = np.ones(ny) * alpha_start
    alpha0 = alpha_start * np.ones(ny)
    dadt = np.zeros(ny) 
    dadt0 = dadt.copy()
    alpha_ges = np.ones((nsteps, ny))
    dadt_ges = np.copy(alpha_ges)*dt # timesteps
    reak_kinetic_ges = np.copy(alpha_ges)
    return k1, k2, alpha, alpha0, dadt, dadt0, alpha_ges, dadt_ges, reak_kinetic_ges

#Reaction kinetics get solved with the regular or advanced Kamal-Souror method with the following function:
def calcReaktionskinetik(ny, dt,  phi, density_M, density_schicht, u0, u, boundary1, boundary2, nsteps, alpha0, dadt0):
    global advancedKS, resinSystem, alpha_start, R
    
    #if "alpha_start" in kwargs:
    #    alpha_start=kwargs["alpha_start"]
    #else:
    #    alpha_start = alpha_start

    if resinSystem==135: # resin system RIMR135-RIMH137
        A1, E1, A2, E2, s, v, R_DUMMY, Htot, _, _, Ad, Ed, alphaf, b, fg, Tg0, Tg00, Lambda = reakParameter_135() # , alpha_start_DUMMY, heizrate_DUMMY
    elif resinSystem==35:  # resin system RIMR035c-RIMH037
        A1, E1, A2, E2, s, v, R_DUMMY, Htot, _, heizrate_DUMMY, Tg0, Tg00 = reakParameter_35() # only regular Kamal-Souror
    elif resinSystem==1037: # resin system RIMR1037-RIMH1037
        raise ValueError("resinSystem==1037 not implemented")
    else:
        raise ValueError("invalid resinSystem: "+str(resinSystem))
    
    alpha = alpha0 + (dadt0*dt) 
    if( (alpha>1).any() ):
        print("dt:"+str(dt))
        print("dadt0:"+str(dadt0))
        print("alpha0:"+str(alpha0))
        raise ValueError("alpha is >1: "+str(alpha))
    
    # kinetically controlled Arrhenius-dependent reaction rate constant
    # Geschwindigkeitskonstante (k_c,1, k_c,2) für chemischen Anteil, vgl Modelle_Regelung_Austausch eq 14
    kc1 = A1 * np.exp(-E1/(R*u0))
    kc2 = A2 * np.exp(-E2/(R*u0))
        
    # warning if Tg00-Tg0<0
    if (Tg00-Tg0<0):
        import warnings
        warnings.warn("Warning...........Tg00-Tg0<0")
    
    Tg = None # initialise
    
    if advancedKS == False: # regular Kamal-Souror method
        k1 = kc1
        k2 = kc2
    else: # advanced Kamal-Souror method: consider the effect of diffusion

        # Glass transition temperature of the resin system in the current state of cure
        # DiBenedetto equation as a model for the change of the glass transition temperature with the degree of cure:
        # Glasübergangstemperatur durch DiBenedetto Gleichung mit globalem alpha, Modelle_Regelung_Austausch eq 17
        Tg = Tg0 + (max(Tg00-Tg0,0) * Lambda * alpha)/(1-(1-Lambda)*alpha) +273.15    
    
        # modify curing kinetics model with the Rabinowitch assumption as diffusion control model (https://doi.org/10.1039/TF9373301225) 
        # to account for the shift from chemically-controlled to diffusion-controlled kinetics
        
        # Diffusion rate constant based on the Huguenin model (*) equation 7, https://doi.org/10.1021/i300017a031)
        # Geschwindigkeitskonstante für diffusionskontrollierten Anteil, vgl. Modelle_Regelung_Austausch eq 15,16
        kd = Ad * np.exp(-Ed/(R*u0)) * np.exp(-b/(alphaf * (u0-Tg)+fg))  # u0 is cure temperature
        
        # Modified reaction rate constant k_i; (https://doi.org/10.1016/j.tca.2015.11.014 equation 6)
        # (reaction constants with an Arrhenius type of dependence with temperature)
        # [Geschwindigkeitskonstante k (k_1,k_2), vgl. Modelle_Regelung_Austausch eq 13]
        k1 = 1/((1/kc1)+(1/kd))
        k2 = 1/((1/kc2)+(1/kd))
    
    # Kamal–Sourour cure kinetics model  (https://doi.org/10.1016/j.tca.2015.11.014 equation 5)
    # Reaktionsgeschwindigkeit/Umsatzrate; 
    #print("calcReaktionskinetik")
    #print("A1: "+str(A1)+" E1: "+str(E1)+" u0: "+str(u0)) # error wenn u0 negativ!?!
    #print("kc1: "+str(kc1)+" kc2: "+str(kc2))#+" kd: "+str(kd))
    #print("s: "+str(s)+" v: "+str(v)+" k1: "+str(k1)+" k2: "+str(k2))
    #print("alpha0: "+str(alpha0)+"alpha: "+str(alpha)+" dadt0: "+str(dadt0))
    #print("...: "+str((1 - alpha)**v))
    dadt = (k1 + (k2 * alpha**s)) * (1 - alpha)**v
    
    if( (dadt*dt>1).any() ):
        print("u0:"+str(u0))
        print("k1:"+str(k1)+" k2:"+str(k2))
        print("alpha**s:"+str(alpha**s))
        print("(1 - alpha)**v:"+str((1 - alpha)**v))
        print("dadt:"+str(dadt))
        print("alpha0:"+str(alpha0))
        print("alpha:"+str(alpha))
        print("advancedKS:"+str(advancedKS))
        print("resinSystem:"+str(resinSystem))
        raise ValueError("dt is "+str(dt)+", dadt is >1: "+str(dadt))
    
    #print("dadt in calcReaktionskinetik: "+str(dadt))
    
    cp_comp = calc_cp_epoxy(u, alpha, ny) #materialparameter.
    
    reak_kinetik = dt * ((dadt * Htot * (1 - phi) * density_M) / (cp_comp * density_schicht))

    return reak_kinetik, alpha, dadt, Tg