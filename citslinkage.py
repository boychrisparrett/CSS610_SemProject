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
    ## Desc: first block of code in "cits-talk" procedure
    ##
    ## Paramters:
    ##    1)
    ##    2)
    ##    3)
    ##
    ## Returns: Nothing
    ## to cits-talk:: ask cits
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
            link.setCboeu(LINK.ORIGIDX,0.5 * (1.5 * eu1 + link.getIntereu()))

            ## Calculate and store the exepected utility of dest's CBO
            #NL: set cboeu2 0.5 * (1.5 * eu2 + intereu)
            link.setCboeu(LINK.DESTIDX,0.5 * (1.5 * eu2 + link.getIntereu()))

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


            #NL: ask end1
            #NL: if empty? [cboeu1] of my-out-links with [citlink? = ticks]:
            if self.getLinksFromNode(t,orig) is None:
                link.setTempEu(0)
            else:
                #NL: set temp-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                link.setTempEu( orig.getMaxOutlinks(t,orig.getUID(),"cboeu") )

                #NL: set minpref min [diffpref1] of my-out-links with citlink? = ticks]
                link.setMinpref( orig.getMinOutlinks(t,orig.getUID(),"diffpref") )


            #NL: ask end2 [
            #NL: if empty? [cboeu1] of my-in-links with [citlink? = ticks]:
            if self.getLinksFromNode(t,dest) is None:
                #NL: set temp-eu 0
                link.setTempEu(0)
            else:
                #NL: set temp-eu max [cboeu2] of my-in-links  with [citlink? = ticks]
                link.setTempEu( dest.getMaxOutlinks(t,dest.getUID(),"cboeu") )

                #NL: set minpref min [diffpref2] of my-in-links with [citlink? = ticks]
                link.setMinpref( dest.getMinOutlinks(t,dest.getUID(),"diffpref") )

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
    #  ask linkcits with [citlink? = ticks] [
    def ManageCurrentLink(self,t,cits):
        for link in self.linkcits[t]:
            orig = cits.getCITS( link.getOrignode() )
            dest = cits.getCITS( link.getDestnode() )
            #if cboeu1 < [temp-eu] of end1 [die]
            if link.getCboeu(LINK_CITS.ORIGIDX) < orig.getTemp_Eu():
                self.linkcits[t].remove(link)

            #if cboeu1 < [own-eu] of end1 [die]
            elif link.getCboeu(LINK_CITS.ORIGIDX) < orig.getOwn(Entity.E_EU):
                self.linkcits[t].remove(link)

            #if cboeu2 <= [own-eu] of end2 [die]
            elif link.getCboeu(LINK_CITS.DESTIDX) < dest.getOwn(Entity.E_EU):
                self.linkcits[t].remove(link)

            #if diffpref2 > [minpref] of end2 [die]
            elif link.getDiffpref(LINK_CITS.DESTIDX) < dest.getMinpref():
                self.linkcits[t].remove(link)

            # ifelse ([temp-eu] of end1 > [own-eu] of end1) and
            #        ([temp-eu] of end2 > [own-eu] of end2)
            elif (orig.getTempEu() > orig.getOwn(Entity.EU)) and (dest.getTempEu() > dest.getOwn(Entity.EU)) :
                #ask end1 [
                #set turcbo 2
                orig.setTurcbo(2)

                #set stakeholder? 1
                orig.setStakeholder(True)

                maxval = self.getMaxOutlinks("cbopref")
                #set own-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setOwn(Entity.PRF, maxval)

                #set sown-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setSown(Entity.PRF, maxval)

                #set cbo-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setCbo(Entity.PRF, maxval)

                #set own-power 1.5 * own-power
                orig.setOwn(Entity.POW, 1.5 * orig.getOwn(Entity.POW))

                #set sown-power max [cbopower] of my-out-links with [citlink? = ticks]
                maxval = self.getMaxOutlinks("cbopower")
                orig.setSown(Entity.POW, maxval)

                #set cbo-power max [cbopower] of my-out-links with [citlink? = ticks]
                orig.setCbo(Entity.POW, maxval)

                maxval = self.getMaxOutlinks("cboeu")
                #set own-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                orig.setOwn(Entity.EU, maxval)

                #set sown-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                orig.setSown(Entity.EU, maxval)

                #set cbo-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                orig.setCbo(Entity.EU, maxval)

                #ask end2 [
                #set turcbo 2
                dest.setTurcbo(2)

                #set stakeholder? 0
                dest.setStakeholder(False)

                #set own-pref [cbo-pref] of other-end
                dest.setOwn(Entity.PRF, orig.getCbo(Entity.PRF))

                #set cbo-pref [cbo-pref] of other-end
                dest.setCbo(Entity.PRF, orig.getCbo(Entity.PRF))

                #set own-power 1.5 * own-power
                dest.setOwn(Entity.POW, 1.5 * dest.getOwn(Entity.POW))

                #set cbo-power 0
                dest.setCbo(Entity.POW, 0)

                maxval = self.getMaxInlinks("cboeu")
                #set own-eu max [cboeu2] of my-in-links with [citlink? = ticks]
                dest.setOwn(Entity.EU, maxval)

                #set cbo-eu max [cboeu2] of my-in-links with [citlink? = ticks]
                dest.setCbo(Entity.EU, maxval)
            else:
                #ask end1 [
                #set turcbo 1
                orig.setTurcbo(1)
                #set own-pref own-pref
                #!!! WHY??? 1 == 1, 2 == 2, etc. No need to assign itself its own value?
                #set own-power own-power
                #!!! WHY??? 1 == 1, 2 == 2, etc. No need to assign itself its own value?

                #ask end2 [
                #set turcbo 1
                dest.setTurcbo(1)
                #set own-pref own-pref
                #!!! WHY??? 1 == 1, 2 == 2, etc. No need to assign itself its own value?
                #set own-power own-power
                #!!! WHY??? 1 == 1, 2 == 2, etc. No need to assign itself its own value?
                self.linkcits[t].remove(link)

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
    # ask linkcits with [citlink? < ticks] [
    def ManagePreviousLink(self, t, cits):
        for link in self.linkcits[t]:
            #ask linkcits with [citlink? < ticks] [
            orig = cits.getCITS( link.getOrignode() )
            dest = cits.getCITS( link.getDestnode() )

            #if [own-pref] of end1 != [own-pref] of end2 [
            if orig.getOwn(Entity.PRF) != dest.getOwn(Entity.PRF):
                #set pref1 [own-pref] of end1
                pref1 = orig.getOwn(Entity.PRF)

                #set power1 [own-power] of end1
                power1 = orig.getOwn(Entity.PRF)

                #set eu1 [own-eu] of end1
                eu1 = orig.getOwn(Entity.EU)

                #set pref2 [own-pref] of end2
                pref2 = dest.getOwn(Entity.PRF)

                #set power2 [own-power] of end2
                power2 = dest.getOwn(Entity.POW)

                #set eu2 [own-eu] of end2
                eu2 = dest.getOwn(Entity.EU)

                #set intereu (power1 + power2) * 1.5 * (100 - abs(pref1 - pref2))
                link.setIntereu ((power1 + power2) * 1.5 * (100 - abs(pref1 - pref2)))

                #set cboeu1 0.5 * (1.5 * eu1 + intereu)
                link.setCboeu(LINK.ORIGIDX,0.5 * (1.5 * eu1 + link.getIntereu()))

                #set cboeu2 0.5 * (1.5 * eu2 + intereu)
                link.setCboeu(LINK.DESTIDX,0.5 * (1.5 * eu2 + link.getIntereu()))

                #set cbopref ((pref1 * power1 + pref2 * power2)/(power1 + power2 + 0.0000001))
                link.setCbo(Entity.PRF,((pref1 * power1 + pref2 * power2)/(power1 + power2 + 0.0000001)))

                #set cbopower (power1 + power2) * 1.5
                link.setCbo(Entity.POW,(power1 + power2) * 1.5)

                #if(cboeu1 < [own-eu] of end1) or (cboeu2 < [own-eu] of end2) [
                if (link.getCboeu(LINK.ORIGIDX) < orig.getOwn(Entity.EU)) or (link.setCboeu(LINK.DESTIDX) < dest.getOwn(Entity.EU)):
                    #ask end1 [
                    #if count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [

                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinkstToNode(t,orig)) == 0:
                        #set turcbo 1
                        orig.setTurcbo(1)

                        #set cbo-pref 0
                        orig.setCbo(Entity.PRF,0)

                        #set cbo-power 0
                        orig.setCbo(Entity.POW,0)

                        #set stakeholder? 0
                        orig.setStakeholder(False)

                        #set own-power own-power / 1.5
                        orig.setOwn(Entity.POW, orig.getOwn(Entity.POW) * 1.5)

                        #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                        orig.setOwn(Entity.EU, 100 * orig.getOwn(Entity.POW))

                        #set shape "circle"
                        orig.setShape('o')
                    #ask end2 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    if len(self.getLinksFromNode(t,dest)) == 0 and len(self.getLinkstToNode(t,dest)) == 0:

                        #set turcbo 1
                        dest.setTurcbo(1)

                        #set cbo-pref 0
                        dest.setCbo(Entity.PRF,0)

                        #set cbo-power 0
                        dest.setCbo(Entity.POW,0)

                        #set stakeholder? 0
                        dest.setStakeholder(False)

                        #set own-power own-power / 1.5
                        dest.setOwn(Entity.POW, dest.getOwn(Entity.POW) * 1.5)

                        #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                        dest.setOwn(Entity.EU, 100 * dest.getOwn(Entity.POW))

                        #set shape "circle"
                        dest.setShape('o')
                    #die
                    self.linkcits[t].remove(link)
                else:
                    #ask end1
                    #ifelse count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinkstToNode(t,orig)) == 0:
                        #set turcbo 2
                        orig.setTurcbo(2)

                        #set stakeholder? 0
                        orig.setStakeholder(False)

                        #set own-pref [cbo-pref] of other-end
                        orig.setOwn(Entity.PRF,dest.getOwn(Entity.PRF))

                        #set cbo-pref [cbo-pref] of other-end
                        orig.setCbo(Entity.PRF,dest.getOwn(Entity.PRF))

                        #set cbo-power 0
                        orig.setCbo(Entity.POW,0)

                        #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                        orig.setOwn(Entity.EU, 100 * dest.getOwn(Entity.POW))
                    else:
                        #set stakeholder? 1
                        orig.setStakeholder(1)

                    #ask end2 [
                    #ifelse count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    if len(self.getLinksFromNode(t,dest)) == 0 and len(self.getLinkstToNode(t,dest)) == 0:
                        #set turcbo 2
                        dest.setTurcbo(2)

                        #set stakeholder? 0
                        dest.setStakeholder(False)

                        #set own-pref [cbo-pref] of other-end
                        dest.setOwn(Entity.PRF, orig.getOwn(Entity.PRF))

                        #set cbo-pref [cbo-pref] of other-end
                        dest.setCbo(Entity.PRF, orig.getOwn(Entity.PRF))

                        #set cbo-power 0
                        dest.setCbo(Entity.POW,0)

                        #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                        dest.setOwn(Entity.EU, 100 * dest.getOwn(Entity.POW))
                    else:
                        #set stakeholder? 1
                        dest.setStakeholder(1)
                    #set hidden? FALSE
                    self.linkcits[t].setHidden(False)

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
    def UpdateCITS(self,cits):
        #ask cits with [stakeholder? = 1] [
        for c in cits:
            if c.getStakeholder():
                #!!! I am not convinced the below is theoretically correct (syntactically ok). Did he really mean to nest them this way? t2 + t3 - own * (t4 + t5 - 1)???
                #set cbo-power = (sum [cbopower] of my-out-links with [citlink? > 0]) + (sum [cbopower] of my-in-links with [citlink? > 0]) - own-power * ((count my-out-links with [citlink? > 0]) + (count my-in-links with [citlink? > 0]) - 1)]

                #t2 = sum [cbopower] of my-out-links with [citlink? > 0]
                #t4 = count my-out-links with [citlink? > 0]
                t2,t4 = self.getSumOutlinksP(Entity.POW)

                #t3 = sum [cbopower] of my-in-links with [citlink? > 0]
                #t5 = count my-in-links with [citlink? > 0]
                t3,t5 = self.getSumInlinksP(Entity.POW)

                c. setCbo(Entity.POW,(t2) + (t3) - own-power * ((t4) + (t5) - 1))


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
    def getLinksToNode(self,t,node):
        ret = []
        for link in linkcits[t]:
            if node == link.getDestnode():
                ret.append(link.getOrignode())
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
    def removeLink(self,t,orig,dest):
        for link in linkcits[t]:
            if self.linkcits[t].getOrignode() == orig and self.linkcits[t].getDestnode() == dest:
                linkcits[t].remove(link)

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
        for i in self.linkcits[t]:
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
        for i in self.linkcits[t]:
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
        for i in self.linkcits[t]:
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
        for i in self.linkcits[t]:
            if i.getDestnode() == node and lv > i.getCbo(param):
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
    def getSumOutlinksP(self, t, node, param):
        lv = 0
        cnt = 0
        for i in self.linkcits[t]:
            if if i.getOrignode() == node and i.getCitlink() > 0:
                lv += i.getCbo(param)
                cnt+=1
        return lv,cnt

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
    def getSumInlinksP(self, t, node, param):
        lv = 0
        cnt = 0
        for i in self.linkcits[t]:
            if i.getDestnode() == node and i.getCitlink() > 0:
                lv += i.getCbo(param)
                cnt+=1
        return lv,cnt