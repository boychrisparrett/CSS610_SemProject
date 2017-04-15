from entity import *
from agent import *

class CITS(Agent):
    def __init__(self,uid,x,y):
        Agent.__init__(self,uid,x,y)

        #Customized
        self.proximity = 0
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

        #OWN VARIABLE GROUP
        self.own = Entity(0,0,0)

        #SOWN VARIABLE GROUP
        self.sown = Entity(0,0,0)

        #CBO VARIABLE GROUP
        self.cbo = Entity(0,0,0)

        #SCBO VARIABLE GROUP
        self.scbo = Entity(0,0,0)

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

    def getOwn(self,x): return self.own.getEntity(x)
    def getSown(self,x): return self.sown.getEntity(x)
    def getCbo(self,x): return self.cbo.getEntity(x)
    def getScbo(self,x): return self.scbo.getEntity(x)

    def setOwn(self,x,v): self.own.setEntity(x,v)
    def setSown(self,x,v): self.sown.setEntity(x,v)
    def setCbo(self,x,v): self.cbo.setEntity(x,v)
    def setScbo(self,x,v): self.scbo.setEntity(x,v)
