##############################################################################
# Author: Christopher M. Parrett
# Homework #2, due 08FEB2017
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
# CLASS::
#
# Purpose:
#
#
class Entity:
    EU = 0
    POW = 1
    PRF = 2
    def __init__(self,eu,power,pref):
        self.pref = 0
        self.power = 0
        self.own_eu = 0
        

    def getEntity(self,x):
        if x == Entity.EU: return self.own_eu
        elif x == Entity.POW: return self.power
        elif x == Entity.PRF: return self.pref


    def setEntity(self,x,v):
        if x == Entity.EU: self.own_eu = v
        elif x == Entity.POW: self.power = v
        elif x == Entity.PRF: self.pref =v
        