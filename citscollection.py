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
import random
from cits import *
from math import sqrt
from statistics import median

##############################################################################
##############################################################################
# CLASS::CITS_Collection
#
# Purpose: Implements the array of CITS turtles
#
class CITS_Collection:
    #Constants that will be set through the interface
    CONST_IDEO_MEAN = 96.0
    CONST_IDEO_SD = 12
    CONST_WEALTH_MEAN = 6.0
    CONST_WEALTH_SD = 13
    CONST_PARTY_NUMBER = 1
    CONST_TALKSPAN = 70
    
    ########################################################################
    #Standard initiatlization routine
    def __init__(self):
        #Declare Collection Variables
        self.cits = []
        self.numcits = 0
        self.locations = []

    ########################################################################
    #Standard GET/SET routins for individual turtle with UID = idx
    def getCITS(self): return self.cits        #Returns entire array
    def getNumCITS(self): return self.numcits
    
    ########################################################################
    #Standard GET/SET routins for individual turtle with UID = idx
    def getCIT(self,idx): return self.cits[idx]
    def setCIT(self,idx,c): self.cits[idx] = c
    
    ##########################################################################
    #def getLOCS(self): return self.locations #returns array of locations
    #def setLOCS(self,l): self.locations = l

    ##----------------------------------------------------------------------
    ## Name: Initialize
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) numcits: The number of agents to instantiate
    ##    2) max_x: The dimension of the cartesian grid in the X direction
    ##    3) max_y: The dimension of the cartesian grid in the Y direction
    ##
    ## Returns: Nothing
    def Initialize(self,numcits,max_x,max_y):
        #Declare Collection Variables
        self.numcits = numcits

        #Instantiate the Grid Coords, X and Y
        xarr = list(range(max_x))
        yarr = list(range(max_y))
        
        #Ensure there is room enough for 1 agent per cell
        if numcits > max_x*max_y:
            print("ERROR: Number of CITS cannot exceed number of cells")
            return -1

        #PIKE previous code would only have a cit per each x value and 1 vaue (e.g. x=1 or y =1 only had one cit - to check each x,y pair)
        #Initiate CITS agents
        for i in range(self.numcits):
            pos = False
            while pos == False: 
                ix = random.choice(xarr)
                #xarr.remove(ix)
                iy = random.choice(yarr)
               # yarr.remove(iy)
                poss_loc =(ix, iy)
                #locs = self.getLOCS()
                if poss_loc not in self.locations:
                    #print (poss_loc, locs)
                    #locs2 = locs.append(poss_loc)
                    #print ('THIS IS LOCS 2:', locs2)
                    self.locations.append(poss_loc)
                    pos = True
        
        
            #Instantiate the agent
            c = CITS(i,ix,iy)
            #print("CITS #%s created at %s %s"%(i,ix,iy))
            
            #Initialize the values
            c.setStakeholder(False)
            c.setParty(random.randint(0,self.CONST_PARTY_NUMBER))

            #set ideo random-normal cit_ideo_mean cit_ideo_sd
            c.setIdeo(random.normalvariate(self.CONST_IDEO_MEAN, self.CONST_IDEO_SD))
            
            c.setOwn(Entity.PRF, c.getIdeo())

            if random.randint(0,100) <= c.getSelectorate():
                c.setSelectorate(True)

            #set wealth random-normal cit_wealth_mean cit_wealth_sd
            c.setWealth(random.normalvariate(self.CONST_WEALTH_MEAN,self.CONST_WEALTH_SD))
            #print("\twith wealth = %s"%c.getWealth())
            
            if c.getSelectorate():
                c.setWealth( c.getWealth() * 1.1)

            #Add CITS to array
            self.cits.append(c)
    ##----------------------------------------------------------------------
    ## Name: InitSatisfaction
    ##
    ## Desc: Sets satisfaction of all agents
    ##
    ## Paramters:
    ##
    ## Returns: Nothing     
    def InitSatisfaction(self):
        #ask cits [...
        for c in self.cits:
            c.setSatisfaction(self.__CalcSatisfaction__(c))
            
    ##----------------------------------------------------------------------
    ## Name: __CalcSatisfaction__
    ##
    ## Desc: PRIVATE function that calculates satisfaction of all agents
    ##
    ## Paramters:
    ##
    ## Returns: Nothing  
    def __CalcSatisfaction__(self,c):
        #set satisfaction wealth * (wealth / median [wealth] of cits) * (ideo / median [ideo] of cits)
        afact= c.getWealth() * (c.getWealth() / self.GetMedian("wealth"))
        bfact= c.getIdeo() / self.GetMedian("ideo")
        return ( afact * bfact )

    ##----------------------------------------------------------------------
    ## Name: UpdatePower
    ##
    ## Desc: Updates the power of all agents
    ##
    ## Paramters:
    ##     1) maxpower: the calculated maximum power of the system
    ##
    ## Returns: Nothing  
    def UpdatePower(self,maxpower):
        for c in self.cits:
            c.setPower( c.getRawpower() / maxpower )
            c.setOwn(Entity.POW, c.getPower())

    ##----------------------------------------------------------------------
    ## Name: UpdateSatisfaction
    ##
    ## Desc: Updates the power of all agents
    ##
    ## Paramters:
    ##     1) base: The economic base level of a government
    ##     2) tax: The tax levied by the government
    ##     3) gov_ideo: the government Ideo
    ##
    ## Returns: Nothing  
    def UpdateSatisfaction(self,base,tax,gov_ideo):
        #ask cits [
        for c in self.cits:
            #let ideo-error -0.02 + random-float 0.04
            ideo_error = -0.02 + (random.random() * 0.04)

            # if selectorate? = 1[set ideo gov-ideo * ideo-error]
            if c.getSelectorate(): c.setIdeo( gov_ideo * ideo_error)

            #if ideo >= 100 [set ideo 99]
            if c.getIdeo() >= 100: c.setIdeo(99)

            #if ideo <= 1 [set ideo 2]
            if c.getIdeo() <= 1: c.setIdeo(2)

            #set own-pref ideo
            c.setOwn(Entity.PRF, c.getIdeo() )

            #set wealth (wealth * (base + random-float ((1 - base) * 2)) * (1 - tax))
            c.setWealth( c.getWealth() * (base + ( random.random() * ((1 - base) * 2)) * (1 - tax)))

            #if selectorate? = 1 [set wealth wealth * 1.1]
            if c.getSelectorate(): c.setWealth( c.getWealth() * 1.1)

            #set satisfaction wealth * (wealth / median [wealth] of cits) * (ideo / median [ideo] of cits)
            c.setSatisfaction( self.__CalcSatisfaction__(c) )

            #set rawpower wealth
            c.setRawpower( c.getWealth() )

    ##----------------------------------------------------------------------
    ## Name: NodesWithinRange
    ##
    ## Desc: Find all nodes with the radius of talkspan 
    ##
    ## Paramters:
    ##    1) orig: Originator node
    ##
    ## Returns: array of agent UIDs within TALKSPAN distance
    def NodesWithinRange(self,orig):
        #Store orginator UID, X and Y coords for calculations
        x1 = orig.getXCor()
        y1 = orig.getYCor()
        uid = orig.getUID()
        #Instantiate array
        ret= []
        #print("Assessing uid ",uid)
        for c in self.cits:
            #create-linkcits-to cits in-radius talkspan with [who != [who] of myself] [
            #Assess all OTHER nodes...
            if uid != c.getUID():
                #Calculate cartesian distance SQRT(X^2+Y^2)
                dist = sqrt(pow((c.getXCor() - x1),2) + pow((c.getYCor() - y1),2))
                #print("\t against: ",c.getUID(), " with dist = ", dist)
                if dist <= self.CONST_TALKSPAN:
                    #Node falls within talkspan distance
                    ret.append(c.getUID())
        return ret

    ##----------------------------------------------------------------------
    ## Name: GetMedian
    ##
    ## Desc: Returns median value of the parameter requested
    ##
    ## Paramters:
    ##    1) fld: The parameter name to search/utlilize
    ##
    ## Returns: median value 
    def GetMedian(self,fld):
        #create empty array for values
        med = []
        
        #build array of values
        if fld == "wealth":
            for i in self.cits: 
                med.append(i.getWealth())
        elif fld == "ideo":
            for i in self.cits: 
                med.append(i.getIdeo())
        #return median of array of values using the statistics.median function
        return median(med)
    
    ##----------------------------------------------------------------------
    ## Name: GetSum
    ##
    ## Desc: Summarizes the values of the parameter requested
    ##
    ## Paramters:
    ##    1) fld: The parameter name to search/utlilize
    ##
    ## Returns: sum of values
    def GetSum(self,fld):
        #Step through each agent in cits and return sum
        med = 0.0
        if fld == "wealth":
            for i in self.cits: med += i.getWealth()
        elif fld == "ideo":
            for i in self.cits: med += i.getIdeo()
        return med
    
    ##----------------------------------------------------------------------
    ## Name: GetMax
    ##
    ## Desc: Finds the maximum value of the parameter requested
    ##
    ## Paramters:
    ##    1) fld: The parameter name to search/utlilize
    ##
    ## Returns: maximum value of parameter
    def GetMax(self, fld):
        #All values must be zero or positive
        mx = -1
        if fld == "proximity":
            #step through each Agent
            for i in self.cits:
                #find a higher value and save
                if mx < i.getProximity(): mx = i.getProximity()
        elif fld == "rawpower":
            #step through each Agent
            for i in self.cits:
                #find a higher value and save
                if mx < i.getRawpower(): mx = i.getRawpower()
        return mx
    
    ##----------------------------------------------------------------------
    ## Name: GetMin
    ##
    ## Desc: Finds the minimum value of the parameter requested
    ##
    ## Paramters:
    ##    1) fld: The parameter name to search/utlilize
    ##
    ## Returns: minimum value of parameter
    def GetMin(self, fld):
        #set a abnormally large number
        min = 100000000
        
        if fld == "proximity":
            #step through each Agent
            for i in self.cits:
                if min > i.getProximity():
                    #found a lower value, save
                    min = i.getProximity()
        elif fld == "rawpower":
            #step through each Agent
            for i in self.cits:
                if min > i.getRawpower():
                    #found a lower value, save
                    min = i.getRawpower()
        return min
