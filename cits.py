##############################################################################
# Authors: Christopher M. Parrett, Tom Pike
# Term Project - Complex Intelligence Preparation of the Battlefield
#
# Computational Social Science 610: Agent Based Modeling and Simulation
# Spring 2017, Department of Computational and Data Sciences,
# Under the most excellent tutelage of Dr. R Axtell, George Mason Univ
#
# Developed on a Windows 10 platform, AMD PhenomII X6 3.3GHz w/ 8GB RAM
# using Python 3.5.2 | Anaconda 4.2.0 (64-bit).
##############################################################################
##############################################################################
from entity import *
from agent import *

#############################################################################
##############################################################################
# CLASS::CITS (derived from Agent)
#
# Purpose: Implements the breed CITS 
#
class CITS(Agent):
    
    ##----------------------------------------------------------------------
    ## Name: __init__
    ##
    ## Desc: Standard initialization routine, derived from Class AGENT.
    ##
    ## Paramters:
    ##    1) uid: Unique Identifier of the object
    ##    2) x: X-Coordinate of the agent in cartesian space
    ##    3) y: Y-Coordinate of the agent in cartesian space    
    ##
    ## Returns: Nothing
    def __init__(self,uid,x,y):
        Agent.__init__(self,uid,x,y)

        #Customized
        self.proximity = 0 # not necessary vestigial attribute
        self.party = 0
        self.selectorate = False
        self.bought = False
        self.satisfaction = 0
        self.edu = 0
        self.edu_scale = 0
        self.rawpower = 0
        self.minpref = 0
        self.temp_eu = 0
        self.stemp_eu = 0
        self.turcbo = 0
        self.sturcbo = False
        #Implemented below as unordered lists of unique objects
        self.inlinks = set() 
        self.outlinks = set() 
        self.stkinlinks = set() 
        self.stkoutlinks = set() 
        self.citlink = 0
        
        #OWN VARIABLE GROUP
        self.own = Entity(0,0,0)

        #SOWN VARIABLE GROUP
        self.sown = Entity(0,0,0)

        #CBO VARIABLE GROUP
        self.cbo = Entity(0,0,0)

        #SCBO VARIABLE GROUP
        self.scbo = Entity(0,0,0)

    #####################################################################
    ## Standard Set Routines, with x = value
    def setProximity(self,x): self.proximity = x
    def setParty(self,x):  self.party = x
    def setSelectorate(self,x):  self.selectorate = x
    def setBought(self,x): self.bought = x
    def setTemp_Eu(self,x): self.temp_eu  = x
    def setSatisfaction (self,x): self.satisfaction = x
    def setEdu(self,x): self.edu  = x
    def setEdu_Scale (self,x): self.edu_scale  = x
    def setRawpower(self,x): self.rawpower = x
    def setMinpref(self,x): self.minpref = x
    def setTurcbo(self,x): self.turcbo = x
    def setStemp_Eu(self,x): self.stemp_eu = x
    def setSturcbo(self,x): self.sturcbo = x
    def setInlinks(self, x): self.inlinks.add(x)           #Set: no need to check for duplicates
    def setOutlinks(self, x): self.outlinks.add(x)         #Set: no need to check for duplicates
    def setStkInlinks(self, x): self.stkinlinks.add(x)     #Set: no need to check for duplicates
    def setStkOutlinks(self, x): self.stkoutlinks.add(x)   #Set: no need to check for duplicates

    #####################################################################
    ## Standard Get Routines
    def getProximity(self): return self.proximity
    def getParty(self): return self.party
    def getSelectorate(self): return self.selectorate
    def getBought(self): return self.bought
    def getTemp_Eu(self): return self.temp_eu
    def getSatisfaction(self): return self.satisfaction
    def getEdu(self): return self.edu
    def getEdu_Scale(self): return self.edu_scale
    def getRawpower(self): return self.rawpower
    def getMinpref(self): return self.minpref
    def getTurcbo(self): return self.turcbo
    def getStemp_Eu(self): return self.stemp_eu
    def getSturcbo(self): return self.sturcbo
    def getInlinks(self): return self.inlinks
    def getOutlinks(self): return self.outlinks
    def getStkInlinks(self): return self.stkinlinks
    def getStkOutlinks(self): return self.stkoutlinks
    
    #####################################################################
    ## Generalized Get Routines using ENTITY class, with x = element
    def getOwn(self,x): return self.own.getEntity(x)
    def getSown(self,x): return self.sown.getEntity(x)
    def getCbo(self,x): return self.cbo.getEntity(x)
    def getScbo(self,x): return self.scbo.getEntity(x)

    #####################################################################
    ## Generalized Set Routines using ENTITY class, with x = element and
    ## v = the value to be stored
    def setOwn(self,x,v): self.own.setEntity(x,v)
    def setSown(self,x,v): self.sown.setEntity(x,v)
    def setCbo(self,x,v): self.cbo.setEntity(x,v)
    def setScbo(self,x,v): self.scbo.setEntity(x,v)
    
    #####################################################################
    ## Remove Links from Set
    def setCitlink(self,v): self.citlink = v
    def getCitlink(self): return self.citlink
    def removeInlink(self,node): 
        if node in self.inlinks: self.inlinks.remove(node)
    def removeOutlink(self,node):
        if node in self.outlinks: self.outlinks.remove(node)
    def removeStkInlink(self,node):
        if node in self.stkinlinks: self.stkinlinks.remove(node)
    def removeStkOutlink(self,node):
        if node in self.stkoutlinks: self.stkoutlinks.remove(node)
