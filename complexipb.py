import random
from citscollection import *
from cits import *
from link_cits import *
from link_stakeholders import *
from citslinkage import *
from stakeholderlinkage import *

global_tax = .018
global_base = 0.685
global_talkspan = 70
global_govt_base_wealth = 5000
global_gov_ideo = 10
global_power_parity = .11
global_threshold = 29

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
        self.govts = Agent(10001,self.centerX,self.centerY) #According to the paper...
        self.linkcits = CITSLinkage(MAX_TICKS)
        self.dlinkstkhldrs = StakeholderLinkage(MAX_TICKS)
        self.ticks = 0
        
        ##DEBUG PURPOSES ONLY
        self.outfile = ""
        

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
        if initnum > (MAX_XCOR * MAX_YCOR):
            print("WARNING: There are more agents than there are spaces!!!")
        self.CITSarr.Initialize(initnum,MAX_XCOR,MAX_YCOR)

        #ask cits [ set satisfaction...]
        self.CITSarr.InitSatisfaction()

        #ask govts [ set wealth...]
        self.govts.setWealth((self.CITSarr.GetSum("wealth") * global_tax) + global_govt_base_wealth)

        #Reset Tick Counter to zero
        self.ticks = 0
        
        #self.linkcits.FormLinks(self.ticks,self.CITSarr)
        self.outfile = open("CITS_OUT.csv",'w')
        self.outfile.write("Time,CITS,Ideo,Power,Wealth,SHldr,Satisfy,CBOPOW,CBOPRF,CBOEU,OwnPOW,OwnPRF,OwnEU\n")


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
        
        #print ('STEP 1')
        #Form links between agents.
        self.linkcits.FormLinks(self.ticks,self.CITSarr)
        
        print ('step 2')
        self.Update()
        print ('step 3')
        self.CITS_Talk()
        print ('step 4')
        #repeat process at stakeholder level
        self.dlinkstkhldrs.FormLinks(self.ticks, self.CITSarr)
        print ('Step 5')
        self.StakeholderTalk()
        #self.Conflict()
        #self.UpdatePlot()
        self.Conflict()
        
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
        self.maxpower = self.CITSarr.GetMax("rawpower")

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
            self.linkcits.UpdateCITS(t, self.CITSarr.getCITS())


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
        #print(self.CITSarr.getNumCITS())
        
        
        #repeat process at stakeholder level- moved in function to ensure stakeholder condition
        self.dlinkstkhldrs.UpdateSHolderLinks(self.ticks, self.CITSarr)
        
        self.dlinkstkhldrs.ManageCurrentLink(self.ticks, self.CITSarr)        
        
        for t in range(self.ticks -1):
            self.dlinkstkhldrs.ManagePreviousLink(t,self.CITSarr)
            
            self.dlinkstkhldrs.UpdateSholdrCITS(t, self.CITSarr.getCITS())
        
        
        outstr=""
        
                 
        '''
        print("CITS#: %s at (%s,%s)"%(c.getUID(),c.getXCor(),c.getYCor()))
        outstr="%s,%s,%s,%s,"%(self.ticks,c.getUID(),c.getXCor(),c.getYCor())
        print("\t  Ideo:",c.getIdeo())
        outstr="%s,%s"%(outstr,c.getIdeo())
        print("\t Power:",c.getPower())
        outstr="%s,%s"%(outstr,c.getPower())
        print("\tWealth:",c.getWealth())
        outstr="%s,%s"%(outstr,c.getWealth())
        print("\t SHldr:",c.getStakeholder())
        outstr="%s,%s"%(outstr,c.getStakeholder())
        print("\tSatisfy:",c.getSatisfaction())
        outstr="%s,%s"%(outstr,c.getSatisfaction())
        print("\tCBO:")
        print("\t\t POW:",c.getCbo(Entity.POW))
        print("\t\t PRF:",c.getCbo(Entity.PRF))
        print("\t\t  EU:",c.getCbo(Entity.EU))
        outstr="%s,%s,%s,%s,"%(outstr,c.getCbo(Entity.POW),c.getCbo(Entity.PRF),c.getCbo(Entity.EU))
        print("\tOwn:")
        print("\t\t POW:",c.getOwn(Entity.POW))
        print("\t\t PRF:",c.getOwn(Entity.PRF))
        print("\t\t  EU:",c.getOwn(Entity.EU))
        outstr="%s,%s,%s,%s\n"%(outstr,c.getOwn(Entity.POW),c.getOwn(Entity.PRF),c.getOwn(Entity.EU))
        self.outfile.write(outstr)'''
        
        
    def Conflict(self):
        #ask cits with [sturcbo? = 1] [
        #    if scbo-power >= sum [own-power] of cits with [sturcbo? != 1] * power-parity and
        #        abs (scbo-pref - global_gov_ideo) > threshold:
        non_sturcbo = 0
        for cit in self.CITSarr.getCITS(): 
            if cit.getSturcbo == False:
                non_sturcbo += cit.getOwn(Enity.POW)
        
        for cit in self.CITSarr.getCITS(): 
            if cit.getSturcbo == True: 
                 #c.setCbo(Entity.POW,(t2) + (t3) - (c.getOwn(Entity.POW)* ((t4) + (t5) - 1)))
                 #[
                #set shape "exclamation"
                #set size 5
                #set color red
            #]
        #]
                 if cit.getCbo(Entity.POW) >= non_sturcbo*global_power_parity:
                     if abs(cits.getCbo(Entity.PREF) - global_gov_ideo) > global_threshold:
                         CONFLICT_FLAG = True
                         cit.shape = '!'
            




if __name__ == '__main__':
    
    sim = ComplexIPBModel()
    
    sim.Setup(300)
    for i in range(3):
        sim.Step()
        print("####################################################################")
        print("####################################################################")
    sim.outfile.close()