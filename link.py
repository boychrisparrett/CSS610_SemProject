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
# CLASS::LINK
#
# Purpose: Implements the NetLogo Link functionality
#
class LINK:
    #Constants to determine originator node and destination node.
    ORIGIDX = 0
    DESTIDX = 1
    
    ##----------------------------------------------------------------------
    ## Name: __init__
    ##
    ## Desc: Standard Initialization Routine
    ##
    ## Paramters:
    ##    1) orig: UID of originator node
    ##    2) dest: UID of destination node
    ##
    ## Returns: Nothing
    def __init__(self,orig,dest):
        self.orignode = orig
        self.destnode = dest
        self.citlink = 0
        self.cbolink = 0
        self.hidden = True
        #PIKE no cboeu
        #self.cboeu = 0
        #PIKE no diffpref, set high since sloce agents are more likely 
        #     they are to form cbo
        #self.diffpref = 100000000.0
        
    #######################################################################
    ## Standard Set Routines
    def setOrignode(self,x): self.orignode = x
    def setDestnode(self,x): self.destnode = x
    def setCitlink(self,x): self.citlink = x
    def setCbolink(self,x): self.cbolink = x
    def setHidden(self,x): self.hidden = x
    #PIKE no cboeu
    #def setCboeu(self,x): self.cboeu = x
    #PIKE no diffpref
    #def setDiffpref(self, x): self.diffpref = x
    

    #######################################################################
    ### Standard Get Routines
    def getOrignode(self): return self.orignode
    def getDestnode(self):  return self.destnode
    def getCitlink(self): return self.citlink
    def getCbolink(self): return self.cbolink
    def getHidden(self): return self.hidden
    #PIKE no cboeu
    #def getCboeu(self): return self.cboeu
    #PIKE no diffpref
    #def getDiffpref(self,x): self.diffpref = x
