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
from link import *

##############################################################################
##############################################################################
# CLASS::LINK_CITS extends Class::LINK
#
# Purpose: Implements the collection of directed CITS links
#
class LINK_CITS(LINK):

    ##----------------------------------------------------------------------
    ## Name: __init__
    ##
    ## Desc: standard initializer, derived from LINK_CITS
    ##
    ## Paramters:
    ##    1) orig: originator node
    ##    2) dest: destination node
    ##
    ## Returns: Nothing
    def __init__(self,orig,dest):
        LINK.__init__(self,orig,dest)
        self.intereu = 0
        self.tempeu = [0,0]
        self.cbo = Entity(0,0,0)

        ###################################################################
        #Below are redundant, but used for traceability with NetLogo Code
        self.pref = [0,0]
        self.power = [0,0]
        self.eu = [0,0]
        self.cboeu = [0,0]
        #PIKE: changed needed ot be like the others
        self.diffpref = [0,0]
        #!!!Was in netlogo code... how is this different from diffpref?
        self.minpref = [0,0]

    ###################################################################
    ### Set/Get Inter/Temp Expected Utility
    def setIntereu(self,x): self.intereu = x
    def getIntereu(self): return self.intereu
    
    def setTempEu(self,idx, x): self.tempeu[idx] = x
    def getTempEu(self, idx): return self.tempeu[idx]

    ###################################################################
    ### Set/Get CBO Expected Utility (EU) / Power (POW) / Pref (PRF)
    def setCbo(self,x,v): self.cbo.setEntity(x,v)
    def getCbo(self,x): return self.cbo.getEntity(x)


    ###################################################################
    ## Below are redundant, but used for traceability with NetLogo Code
    ## allows the link to store the variables for each of its nodes
    def setCboeu(self,idx,x): self.cboeu[idx] = x
    def setPref(self,idx,x): self.pref[idx] = x
    def setPower(self,idx,x): self.power[idx] = x
    def setEu(self,idx,x): self.eu[idx] = x
    def setDiffpref(self,idx, x): self.diffpref[idx] = x
    def setMinpref(self,idx, x): self.minpref[idx] = x

    def getCboeu(self,idx): return self.cboeu[idx]
    def getPref(self,idx): return self.pref[idx]
    def getPower(self,idx): return self.power[idx]
    def getEu(self,idx): return self.eu[idx]
    def getDiffpref(self,idx): return self.diffpref[idx]
    def getMinpref(self,idx): return self.minpref[idx]