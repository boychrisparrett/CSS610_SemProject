
# coding: utf-8

# In[3]:

import random
from cits import *
from govts import *
from link_cits import *
from link_stakeholders import *

global_tax = 0
global_base = 0
global_talkspan = 10
global_govt_base_wealth = 0
global_gov_ideo = 90

MAX_XCOR = 100
MAX_YCOR = 100
MAX_TICKS = 24
CONFLICT_FLAG = False


class ComplexIPBModel:
    def __init__(self):
        self.price = 0
        self.supply = 0
        self.maxprox = 0
        self.maxpower = 0
        self.centerX = int(MAX_XCOR/2)
        self.centerY = int(MAX_YCOR/2)
        self.CITSarr = CITS_Collection()
        self.govts = Agent()
        self.linkcits = CITSLinkage(MAX_TICKS)
        self.dlinkstkhldrs = StakeholderLinkage()
        self.ticks = 0

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1)
    ##    2)
    ##    3)
    ##
    ## Returns: Nothing
    def Setup(self,initnum):
        #clear-all
        self.__init__()

        #create-govts 1 [...]
        self.govts.setStakeholder(True)
        self.govts.setHidden(True)

        #create-cits initial-number
        self.CITSarr.Initialize(initnum,max_x,max_y)

        #ask cits [ set satisfaction...]
        self.CITSarr.InitSatisfaction()

        #ask govts [ set wealth...]
        self.govts.setWealth((self.CITSarr.GetSum("wealth") * global_tax) + global_govt_base_wealth)

        self.ticks()

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1)
    ##    2)
    ##    3)
    ##
    ## Returns: Nothing
    def Step(self):
        if self.ticks >= MAX_TICKS or CONFLICT_FLAG:
            return -1

        #think this needs to only be called once... moved up from
        self.linkcits.FormLinks(self,self.ticks,self.CITSarr)

        self.Update()
        self.CITS_Talk()
        self.StakeholderTalk()
        self.Conflict()
        self.UpdatePlot()

        self.ticks += 1

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1)
    ##    2)
    ##    3)
    ##
    ## Returns: Nothing
    def Update(self):
        #set maxprox max [proximity] of cits
        self.maxprox = self.CITSarr.getMax("proximity")

        self.CITSarr.UpdateSatisfaction(global_base,global_tax,global_gov_ideo)

        #set maxpower max [rawpower] of cits
        self.maxpower = self.CITSarr.getMax("rawpower")

        #ask cits [...
        self.CITSarr.UpdatePower(self.maxpower)

        #ask govts [...
        #  set wealth ((sum ([wealth] of cits) * tax) + Government-Base-Wealth)
        govts.setWealth( (self.CITSarr.GetSum("wealth") * global_tax) + global_govt_base_wealth )
        govts.setPower( govts.getWealth() )

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1)
    ##    2)
    ##    3)
    ##
    ## Returns: Nothing
    def CITS_Talk(self):

        #Step through each node in the CITS array
        ##NL: create-linkcits-to cits in-radius talkspan with [who != [who] of myself]
        ## ^^^^ MOVED UP FOR EFFICIENCY ^^^^ ##

        #!!! think this needs to only be called once... but in netlogo model, it gets called every iteration... results in many links.
        self.linkcits.UpdateLinks(self.ticks,self.CITSarr)

        #ask linkcits with [citlink? = ticks]
        self.linkcits.ManageCurrentLink(self.ticks,self.CITSarr)

        #ask linkcits with [citlink? < ticks]
        for t in range(self.ticks - 1):
            self.linkcits.ManagePreviousLink(t,self.CITSarr)

        #ask cits with [stakeholder? = 1] [
        self.linkcits.UpdateCITS(t,self.CITSarr))



    def StakeholderTalk(self):

        pass

    def Conflict(self):
        ask cits with [sturcbo? = 1] [
            if scbo-power >= sum [own-power] of cits with [sturcbo? != 1] * power-parity and
                abs (scbo-pref - global_gov_ideo) > threshold:
            [
                set shape "exclamation"
                set size 5
                set color red
            ]
        ]



# In[ ]:



