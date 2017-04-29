##############################################################################
# Authors: Christopher M. Parrett, Tom Pike
# Term Project - Complex Intelligence Preparation of the Battlefield
# Computational Social Science 610: Agent Based Modeling and Simulation
# Spring 2017, Department of Computational and Data Sciences,
# Under the most excellent tutelage of Dr. R Axtell, George Mason Univ
#
# Developed on a Windows 10 platform, AMD PhenomII X6 3.3GHz w/ 8GB RAM
# using Python 3.5.2 | Anaconda 4.2.0 (64-bit).
##############################################################################
##############################################################################

##############################################################################
##############################################################################
# CLASS:: Entity
#
# Purpose: Simplifies the maintenance of the three core elements behind the 
#          models entities: Expected Utility (EU), Power (POW), and 
#          Preference(PRF).
#
class Entity:
    EU = 0     #Expected Utility
    POW = 1    #Power
    PRF = 2    #Preference
    
    ##----------------------------------------------------------------------
    ## Name: __init__
    ##
    ## Desc: Standard Initialization
    ##
    ## Parameters:
    ##     1) eu: Expected Utility (Entity.EU)
    ##     2) power: Power (Entity.POW)
    ##     3) pref: Preference(Entity.PRF)
    def __init__(self,eu,power,pref):
        self.pref = pref
        self.power = power
        self.own_eu = eu
        
    ##----------------------------------------------------------------------
    ## Name: getEntity
    ##
    ## Desc: Generalized GET routine
    ##
    ## Paramters:
    ##    1) x: Entity element requested
    ##
    ## Returns: float
    def getEntity(self,x):
        if x == Entity.EU: return self.own_eu
        elif x == Entity.POW: return self.power
        elif x == Entity.PRF: return self.pref

    ##----------------------------------------------------------------------
    ## Name: setEntity
    ##
    ## Desc: Generalized SET routine
    ##
    ## Paramters:
    ##    1) x: Entity element to be set
    ##    2) x: Entity element value
    ##
    ## Returns: Nothing
    def setEntity(self,x,v):
        if x == Entity.EU: self.own_eu = v
        elif x == Entity.POW: self.power = v
        elif x == Entity.PRF: self.pref =v
        