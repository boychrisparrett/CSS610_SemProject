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

import random
from cits import *
from math import sqrt
import numpy as np

global_cit_ideo_mean = 10.0
global_cit_ideo_sd = 0.2
global_cit_wealth_mean = 10.0
global_cit_wealth_sd = 0.2
global_party_number = 1
global_talkspan = 4

##############################################################################
##############################################################################
# CLASS::
#
# Purpose:
#
#
class CITS_Collection:

    def __init__(self):
        #Declare Collection Variables
        self.cits = []
        self.numcits = 0

    def getCITS(self,idx): return self.cits[idx]
    def setCITS(self,idx,c): self.cits[idx] = c

    def getNumCITS(self): return self.numcits

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
    def Initialize(self,numcits,max_x,max_y):
        #Declare Collection Variables
        self.numcits = numcits

        xarr = list(range(max_x))
        yarr = list(range(max_y))

        if numcits > max_x*max_y:
            print("ERROR: Number of CITS cannot exceed number of cells")
            return -1

        #Initiate CITS
        for i in range(self.numcits):
            ix = random.choice(xarr)
            xarr.remove(ix)
            iy = random.choice(yarr)
            yarr.remove(iy)

            c = CITS(i,ix,iy)
            c.setStakeholder(False)
            c.setParty(random.randint(0,global_party_number))

            #########################
            ###!!!CORRECT BELOW!!!###
            c.setIdeo(random.normalvariate(global_cit_ideo_mean, global_cit_ideo_sd))
            c.setOwn(Entity.PRF, c.getIdeo())
            #########################

            if random.randint(0,100) <= c.getSelectorate():
                c.setSelectorate(True)

            #set wealth random-normal cit_wealth_mean cit_wealth_sd
            c.setWealth(random.normalvariate(global_cit_wealth_mean,global_cit_wealth_sd))

            if c.getSelectorate():
                c.setWealth( c.getWealth() * 1.1)

            #Add CITS to array
            self.cits.append(c)

    def InitSatisfaction(self):
        #ask cits [...
        for c in self.cits:
            c.setSatisfaction(self.__CalcSatisfaction__(c))

    def __CalcSatisfaction__(self,c):
        #set satisfaction wealth * (wealth / median [wealth] of cits) * (ideo / median [ideo] of cits)
        afact= c.getWealth() * (c.getWealth() / self.GetMedian("wealth"))
        bfact= c.getIdeo() / self.GetMedian("ideo")
        return ( afact * bfact )


    def UpdatePower(self,maxpower):
        for c in self.cits:
            c.setPower( c.getRawpower() / maxpower )
            c.setOwn(Entity.POW, c.getPower())

    def UpdateSatisfaction(self,base,tax,gov_ideo):
        #ask cits [
        for c in self.cits:
            #let ideo-error -0.02 + random-float 0.04
            ideo_error = -0.02 + (random.random() * 0.04)

            # if selectorate? = 1[set ideo gov-ideo * ideo-error]
            if c.getSelectorate(): c.setIdeo( gov_ideo * ideo_error)

            #if ideo >= 100 [set ideo 99]
            if c.getIdeo() >= 100: m_i.setIdeo(99)

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


    def NodesWithinRange(self,orig):
        x1 = orig.getXCor()
        y1 = orig.getYCor()
        uid = orig.getUID()

        ret= []
        #ask c [
        print("Assessing uid ",uid)
        for c in self.cits:
            #create-linkcits-to cits in-radius talkspan with [who != [who] of myself] [
            if uid != c.getUID():
                dist = sqrt(pow((c.getXCor() - x1),2) + pow((c.getYCor() - y1),2))
                print("\t against: ",c.getUID(), " with dist = ", dist)
                if dist <= global_talkspan:
                    ret.append(c.getUID())
        return ret


    def GetMedian(self,fld):
        med = 0.0
        if fld == "wealth":
            for i in self.cits: med += i.getWealth()
        elif fld == "ideo":
            for i in self.cits: med += i.getIdeo()
            ### FIX... MEDIAN, NOT MEAN
        return (med / len(self.cits))

    def GetSum(self,fld):
        med = 0.0
        if fld == "wealth":
            for i in self.cits: med += i.getWealth()
        elif fld == "ideo":
            for i in self.cits: med += i.getIdeo()
        return med

    def GetMax(self, marr, fld):
        mx = -1
        if fld == "proximity":
            for i in self.cits:
                if mx < i.getProximity(): mx = i.getProximity()
        elif fld == "rawpower":
            for i in self.cits:
                if mx < i.getRawpower(): mx = i.getRawpower()
        return mx

    def GetMin(self, fld):
        min = 10000000
        if fld == "proximity":
            for i in self.cits:
                if min > i.getProximity():
                    min = i.getProximity()
        elif fld == "rawpower":
            for i in self.cits:
                if min > i.getRawpower():
                    min = i.getRawpower()
        return min
