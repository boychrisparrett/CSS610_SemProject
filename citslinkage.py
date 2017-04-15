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

from link_cits import *
from cits import *

##############################################################################
##############################################################################
# CLASS::
#
# Purpose:
#
#

class CITSLinkage:

    def __init__(self,max_t):
        self.linkcits = {}

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
    def FormLinks(self,t,cits):
        links = []
        for ci in cits:
            #get nodes UIDs within range of ci
            ret = ci.NodesWithinRange()
            for l in range(len(ret)):
               links.append( LINK_CITS(ci,ret[l]) )
               links[l].setHidden(True)
        self.linkcits[t] = links

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
    def UpdateLinks(self,t,cits):
        #NL: set citlink? ticks  ***NOT NEEDED... INFERRED***
        for link in self.linkcits[t]:
            #For readability, get origin and destination node of the link
            orig = cits.getCITS( link.getOrignode() )
            dest = cits.getCITS( link.getDestnode() )

            ## Get the pref, power, and EU of Orig/end1
            #NL: set pref1 [own-pref] of end1
            pref1 = orig.getOwn(Entity.E_PRF)
            #NL: set power1 [own-power] of end1
            power1 = orig.getOwn(Entity.E_POW)
            #NL: set eu1 [own-eu] of end1
            eu1 =orig.getOwn(Entity.E_EU)

            ## Get the pref, power, and EU of Dest/end2
            #NL: set pref2 [own-pref] of end2
            pref2 = dest.getOwn(Entity.E_PRF)
            #NL: set power2 [own-power] of end2
            power2 = dest.getOwn(Entity.E_POW)
            #NL: set eu2 [own-eu] of end2
            eu2 = dest.getOwn(Entity.E_EU)

            ## Calculate and store the intermediate expected utility
            #NL: set intereu (power1 + power2) * 1.5 * (100 - abs(pref1 - pref2))
            link.setIntereu(power1 + power2) * 1.5 * 1.5 * (100 - abs(pref1 - pref2))

            ## Calculate and store the exepected utility of orig's CBO
            #NL: set cboeu1 0.5 * (1.5 * eu1 + intereu)
            link.setCboeu(LINK.ORIGIDX,0.5 * (1.5 * eu1 + link.getIntereu())

            ## Calculate and store the exepected utility of dest's CBO
            #NL: set cboeu2 0.5 * (1.5 * eu2 + intereu)
            link.setCboeu((LINK.DESTIDX,0.5 * (1.5 * eu2 + link.getIntereu())

            ## Calculate and store the preference of CBO
            #NL: set cbopref
            link.setCbo(Entity.E_PRF,((pref1 * power1 + pref2 * power2) / (power1 + power2 + 0.0000001)))

            ## Calculate and store the power of CBO
            #NL: set cbopower
            link.setCbo(Entity.E_POW,(power1 + power2) * 1.5)

            ## Calculate and store the expected utility of CBO
            #NL: set cboeu
            link.setCbo(Entity.E_EU, cbopower * (100 - abs (cbopref - cbopref)))

            ## cboeu12 is never used in the algorithm... skipping for now
            #NL: ;;set cboeu12 0.5 * (eu1 + intereu) + 0.5 * (eu2 + intereu)

            ## Calculate and store the differential preferences
            #NL: set diffpref1
            link.setDiffpref(LINK.ORIGIDX, abs(link.getCbo(Entity.E_PRF) - pref1))
            #NL: set diffpref2
            link.setDiffpref(LINK.DESTIDX, abs(link.getCbo(Entity.E_PRF) - pref2))

  ###__> IMPLEMENT <__###
            #NL: ask end1
            #NL: if empty? [cboeu1] of my-out-links with [citlink? = ticks]:
            if getLinksFromNode(t,orig) is None:
                link.setTempEu(0)
            else:
                #NL: set temp-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                orig.getMaxOutlinks(t,c.getUID(),"cboeu")
                    #NL: set minpref min [diffpref1] of my-out-links with [citlink? = ticks]
                    c.getMinOutlinks(t,c.getUID(),"diffpref")
            #NL: ask end2 [
            #NL: if empty? [cboeu1] of my-in-links with [citlink? = ticks]:
                if getLinksToNode(t,c) is None:
            #NL:          set temp-eu 0
            #else:
            #NL:          set temp-eu max [cboeu2] of my-in-links  with [citlink? = ticks]
            #NL:          set minpref min [diffpref2] of my-in-links with [citlink? = ticks]

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
    def ManageLinks(self,t,cits):
        for link in self.linkcits[t]:
            orig = link.getCITS( link.getOrignode() )
            dest = link.getCITS( link.getDestnode() )

            if link.getCboeu(LINK_CITS.ORIGIDX) < cits[orig].getTemp_Eu():
                self.linkcits[t].remove(link)
                break

            if link.getCboeu(LINK_CITS.ORIGIDX) < cits[orig].getOwn(Entity.E_EU):
                self.linkcits[t].remove(link)
                break

            if link.getCboeu(LINK_CITS.DESTIDX) < cits[dest].getOwn(Entity.E_EU):
                self.linkcits[t].remove(link)
                break

            if link.getDiffpref(LINK_CITS.DESTIDX) < cits[dest].getMinpref():
                self.linkcits[t].remove(link)
                break

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
    def getLinksFromNode(self,t,node):
        ret = []
        for link in linkcits[t]:
            if node == link.getOrignode():
                ret.append(link.getDestnode())

        return ret

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
    def removeLink(self,t,orig,dest)
        self.dlinkcits[t][orig].remove(dest)

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
    def getCurrentMaxOutlinks(self, t, node, param):
        lv = 0.0
        for i in self.dlinkcits[t]:
            if i.getOrignode() == node and lv < i.getCbo(param):
                    lv = i.getCbo(param)
        return lv

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
    def getCurrentMaxInlinks(self, t, node, param):
        lv = 0.0
        for i in self.dlinkcits[t]:
            if i.getDestnode() == node and lv < i.getCbo(param):
                lv = i.getCbo(param)
        return lv

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
    def getCurrentMinOutlinks(self, t, node, param):
        lv = 100000000.0
        for i in self.dlinkcits[t]:
            if i.getOrignode() == node and lv > i.getCbo(param):
                    lv = i.getCbo(param)
        return lv

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
    def getCurrentMinInlinks(self, t, node, param):
        lv = 100000000.0
        for i in self.dlinkcits[t]:
            if i.getDestnode() == node and lv > i.getCbo(param):
                lv = i.getCbo(param)
        return lv
