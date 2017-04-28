import random
from cits import *
from link_cits import *
from link_stakeholders import *
from citslinkage import *
from stakeholderlinkage import *

global_tax = .018
global_base = 0.685
global_talkspan = 50
global_govt_base_wealth = 5000
global_gov_ideo = 10

MAX_XCOR = 101
MAX_YCOR = 101
MAX_TICKS = 24
CONFLICT_FLAG = False


class ComplexIPBModel:
    def __init__(self):
        self.price = 0
        self.supply = 0
        ##self.maxprox = 0 # not needed vestigial code
        self.maxpower = 0
        self.centerX = int(MAX_XCOR/2)
        self.centerY = int(MAX_YCOR/2)
        self.CITSarr = CITS_Collection()
        self.govts = Agent(100,self.centerX,self.centerY) #According to the paper...
        self.linkcits = CITSLinkage(MAX_TICKS)
        self.dlinkstkhldrs = StakeholderLinkage(MAX_TICKS)
        self.ticks = 0

    ##----------------------------------------------------------------------
    ## Name: Setup
    ##
    ## Desc: Initializes model 
    ##
    ## Paramters:
    ##    1) initnum - initial number of agents
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
        self.CITSarr.Initialize(initnum,MAX_XCOR,MAX_YCOR)

        #ask cits [ set satisfaction...]
        self.CITSarr.InitSatisfaction()

        #ask govts [ set wealth...]
        self.govts.setWealth((self.CITSarr.GetSum("wealth") * global_tax) + global_govt_base_wealth)
		
		#Reset Tick Counter to zero
        self.ticks = 0

    ##----------------------------------------------------------------------
    ## Name: step
    ##
    ## Desc: steps through the key modules of the model -
    ##       (1) Updates
    ##       (2) CITS_TALK
    ##       (3) Stalkeholder talk
    ##       (4) Conflict
    ##       (5) Update Plot
    ##
    ## Paramters:
    ##    1) ticks- counter of how many times step method has run
    ##    2) CITSarr.cits - list of agent (citizens) in model
    ##    3)
    ##
    ## Returns: Nothing
    def Step(self):
        if self.ticks >= MAX_TICKS or CONFLICT_FLAG:
            return -1

        # PIKE removed first self, I believe it is ok but not sure
        #think this needs to only be called once... moved up from
        #print (self.CITSarr.cits)
        self.linkcits.FormLinks(self.ticks,self.CITSarr)

        self.Update()
        self.CITS_Talk()
        self.StakeholderTalk()
        #self.Conflict()
        #self.UpdatePlot()

        self.ticks += 1

    ##----------------------------------------------------------------------
    ## Name: Update 
    ##
    ## Desc: 1st module in step function updates all agents (citizens and govt) wealth power and satisfication
    ##       attributes, the main variables to determine population satisifaction towards the government and conflict onset
    ##
    ## Paramters:
    ##    1) base - input, simulates base wealth of each citizen
    ##    2) tax - input, simulates tax rate og govt to determines its wealth 
    ##    3) gov_ideo - input, simulates governemtn ideology on a spectrum of 0 to 100
    ##    4) maxpower - gets the maxpower of the citizne population 
    ##    5) Getsum('wealth") calculates the wealth of the citizens to determine govt wealth
    ##    6) govts.getWealth() calculates wealth of government
    ##
    ## Returns: Nothing
    def Update(self):
        # Pike vestigial code --removed
        #set maxprox max [proximity] of cits
        #self.maxprox = self.CITSarr.getMax("proximity")

        self.CITSarr.UpdateSatisfaction(global_base,global_tax,global_gov_ideo)

        #set maxpower max [rawpower] of cits
        #PIKE RUN DEBUG PRINT FOR THIS
        self.maxpower = self.CITSarr.GetMax(self, "rawpower")

        #ask cits [...
        self.CITSarr.UpdatePower(self.maxpower)

        #ask govts [...
        #  set wealth ((sum ([wealth] of cits) * tax) + Government-Base-Wealth)
        self.govts.setWealth( (self.CITSarr.GetSum("wealth") * global_tax) + global_govt_base_wealth )
        self.govts.setPower( self.govts.getWealth() )

    ##----------------------------------------------------------------------
    ## Name: CITS_Talk
    ##
    ## Desc: citizen agents conduct pairwise comparison of all agents in talkspan range to determine if they should form a cbo 
    ##
    ## Parameters:
    ##    1) ticks - number of times step method has been run
    ##    2) CITSarr - citizen objects in list
    ##    3) 
    ##
    ## Returns: Nothing
    def CITS_Talk(self):

        #Step through each node in the CITS array
        ##NL: create-linkcits-to cits in-radius talkspan with [who != [who] of myself]
        ## ^^^^ MOVED UP FOR EFFICIENCY ^^^^ ##

        #!!! think this needs to only be called once... but in netlogo model, it gets called 
		#!!! every iteration... results in many links.
        self.linkcits.UpdateLinks(self.ticks,self.CITSarr)

        #ask linkcits with [citlink? = ticks]
        self.linkcits.ManageCurrentLink(self.ticks,self.CITSarr)

        #ask linkcits with [citlink? < ticks]
        for t in range(self.ticks - 1):
            self.linkcits.ManagePreviousLink(t,self.CITSarr)

            #ask cits with [stakeholder? = 1] [
            self.linkcits.UpdateCITS(t,self.CITSarr)


    ##----------------------------------------------------------------------
    ## Name: StakeholderTalk
    ##
    ## Desc: cbos talk and determine if they should form alliances
    ##
    ## Parameters:
    ##    1) ticks - number of times step method has been run
    ##    2) CITSarr - citizen objects in list
    ##    3) 
    ##
    ## Returns: Nothing


    def StakeholderTalk(self):

        for c in self.CITSarr.cits: 
            print (c)
    

    '''
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

    '''

# In[ ]:

if __name__ == '__main__':
    
    sim = ComplexIPBModel()
    
    sim.Setup(10)
    sim.Step()

