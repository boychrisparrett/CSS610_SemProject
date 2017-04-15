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
class LINK:
    ORIGIDX = 0
    DESTIDX = 1

    ### Standard Initialization Routine
    def __init__(self,orig,dest):
        self.orignode = orig
        self.destnode = dest
        self.citlink = 0
        self.cbolink = 0
        self.hidden = True

    ### Standard Set Routines
    def setOrignode(self,x): self.orignode = x
    def setDestnode(self,x): self.destnode = x
    def setCitlink(self,x): self.citlink = x
    def setCbolink(self,x): self.cbolink = x
    def setHidden(self,x): self.hidden = x

    ### Standard Get Routines
    def getHidden(self): return self.hidden
    def getOrignode(self): return self.orignode
    def getDestnode(self):  return self.destnode
    def getCitlink(self): return self.citlink
    def getCbolink(self): return self.cbolink
