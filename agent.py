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

##############################################################################
##############################################################################
# CLASS::Agent
#
# Purpose: Implements the base functionality of a NetLogo "Turtle"
#
#
class Agent:
 
    ##----------------------------------------------------------------------
    ## Name: __init__
    ##
    ## Desc: Standard initialization routine of Class AGENT
    ##
    ## Paramters:
    ##    1) uid: Unique Identifier of the object
    ##    2) x: X-Coordinate of the agent in cartesian space
    ##    3) y: Y-Coordinate of the agent in cartesian space
    ##
    ## Returns: Nothing
    def __init__(self,uid,x,y):
        self.UID = uid
        self.color = "#FFFFFF" #White
        self.shape = 'o'       #Circle
        self.xcor = x
        self.ycor = y
        self.hidden = False
        self.stakeholder = False
        self.ideo =0.0    #random.gauss(cit_ideo_mean, cit_ideo_sd)
        self.wealth = 0.0 #random.gauss(cit_wealth_mean, cit_wealth_sd)
        self.power = 0

    #####################################################################
    ## Standard Set Routines
    def setUID(self,x): self.UID = x
    def setIdeo(self,x): self.ideo = x
    def setWealth(self,x): self.wealth = x
    def setPower(self,x): self.power = x
    def setStakeholder(self,x): self.stakeholder = x
    def setColor(self,x): self.color = x
    def setXCor(self,x): self.xcor = x
    def setYCor(self,x): self.ycor = x
    def setHidden(self,x): self.hidden = x

    #####################################################################
    ## Standard Get Routines
    def getUID(self): return self.UID
    def getIdeo(self): return self.ideo
    def getWealth(self): return self.wealth
    def getPower(self): return self.power
    def getStakeholder(self): return self.stakeholder
    def getColor(self): return self.color
    def getXCor(self): return self.xcor
    def getYCor(self): return self.ycor
    def getHidden(self): return self.hidden
