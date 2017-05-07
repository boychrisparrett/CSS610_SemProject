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
#for debug
import time

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
        #mjr_time_start = time.time()
        #print("\t***Starting CITS FormLinks")
        for ci in cits.getCITS():
            #inner_time_start = time.time()
            #get nodes UIDs within range of ci
            #PIKE had to change  from "ret = ci.NodesWithinRange()" call function in citslinkage
            ret = cits.NodesWithinRange(ci)
            #PIKE change to return agent ID so Update links line: 87---orig = cits.getCIT(link.getOrignode() ) below to pass in ID versus object
            #print("There are %s nodes within reach."%len(ret))
            for l in range(len(ret)):

                #add to self.linkcits
                links.append(LINK_CITS(ci.getUID(),ret[l]))
                links[l].setHidden(True)
                
                #append to other citizens outlinks
                ci.setOutlinks(ret[l])
                ci.setCitlink(1)  #!!! not sure this is right... but seems so
                
                #create inlinks at ret[l]
                cits.getCIT(ret[l]).setInlinks(ci.getUID())
                cits.getCIT(ret[l]).setCitlink(1)  #!!! not sure this is right... but seems so
                
                #print("\tLength of outlinks: %s\n\tLength of inlinks: %s"%(len(ci.getOutlinks()),len(cits.getCIT(ret[l]).getInlinks())))
                
                #outs.append(LINK_CITS(ci.UID, ret[l]))
            #inner_time_stop = time.time()
            #print("Inner Loop #%s took %s seconds."%(ci.getUID(),inner_time_stop-inner_time_start))
        mjr_time_stop = time.time()
        self.linkcits[t] = links
        #print ('\tTOTAL LINKS FORMED: %s in %s seconds'%(len(self.linkcits[t]),mjr_time_stop-mjr_time_start))
        #print("\tEnding CITS FormLinks in %s seconds",(time.time()-mjr_time_start))
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
       
        #print ('\t***Start UpdateLinks')
        starttime = time.time()
        count = 0
        for link in self.linkcits[t]:
            #For readability, get origin and destination node of the link
            #PIKE UPDATED TO PASS IN citizen versus citizne list 
            # FROM  orig = cits.getCITS( link.getOrignode() ) to  orig = cits.getCIT( link.getOrignode() )
            
            #print ('step 3a-1')
            orig = cits.getCIT(link.getOrignode())
            dest = cits.getCIT(link.getDestnode())

            ## Get the pref, power, and EU of Orig/end1
            #NL: set pref1 [own-pref] of end1
            pref1 = orig.getOwn(Entity.PRF)
            #NL: set power1 [own-power] of end1
            power1 = orig.getOwn(Entity.POW)
            #NL: set eu1 [own-eu] of end1
            eu1 =orig.getOwn(Entity.EU)

            ## Get the pref, power, and EU of Dest/end2
            #NL: set pref2 [own-pref] of end2
            pref2 = dest.getOwn(Entity.PRF)
            #NL: set power2 [own-power] of end2
            power2 = dest.getOwn(Entity.POW)
            #NL: set eu2 [own-eu] of end2
            eu2 = dest.getOwn(Entity.EU)
            
            # NL: set cbopower (power1 + power2) * 1.5 
            cbopower = (power1 + power2) * 1.5
                       
            #NL:  set cbopref ((pref1 * power1 + pref2 * power2)/(power1 + power2 + 0.0000001))
            cbopref = (pref1 * power1 + pref2 * power2)/(power1 + power2 + 0.0000001)

            #print ("POWER:", power1, power2)
            #print ("PREF", pref1, pref2)
            
            
            ## Calculate and store the intermediate expected utility
            #NL: set intereu (power1 + power2) * 1.5 * (100 - abs(pref1 - pref2))
            #### PIKE Had an extra 1.5....removed TDP
            link.setIntereu( (power1 + power2) * 1.5 * (100 - abs(pref1 - pref2)))
            
            ## Calculate and store the exepected utility of orig's CBO
            #NL: set cboeu1 0.5 * (1.5 * eu1 + intereu)
            link.setCboeu(LINK.ORIGIDX,0.5 * (1.5 * eu1 + link.getIntereu()))
            #print ("CBOUEU!!!:", link.getCboeu(LINK.ORIGIDX))
            
            ## Calculate and store the exepected utility of dest's CBO
            #NL: set cboeu2 0.5 * (1.5 * eu2 + intereu)
            link.setCboeu(LINK.DESTIDX,0.5 * (1.5 * eu2 + link.getIntereu()))

            ## Calculate and store the preference of CBO
            #NL: set cbopref
            # PIKE Changed from E_PRF %POW %EU to PRF % POW %EU
            link.setCbo(Entity.PRF,((pref1 * power1 + pref2 * power2) / (power1 + power2 + 0.0000001)))

            ## Calculate and store the power of CBO
            #NL: set cbopower
            link.setCbo(Entity.POW,(power1 + power2) * 1.5)

            ## Calculate and store the expected utility of CBO
            #NL: set cboeu
            link.setCbo(Entity.EU, cbopower * (100 - abs (cbopref - cbopref)))

            ## cboeu12 is never used in the algorithm... skipping for now
            #NL: ;;set cboeu12 0.5 * (eu1 + intereu) + 0.5 * (eu2 + intereu)

            ## Calculate and store the differential preferences
            #NL: set diffpref1
            # PIKE Changed from E_PRF %POW %EU to PRF % POW %EU
            link.setDiffpref(LINK.ORIGIDX, abs(link.getCbo(Entity.PRF) - pref1))
            orig.setDiffpref(abs(link.getCbo(Entity.PRF) - pref1)) 
            
            #print ("THINK IS DIFFPREF !:", link.getDiffpref(LINK.ORIGIDX))
            #NL: set diffpref2
            link.setDiffpref(LINK.DESTIDX, abs(link.getCbo(Entity.PRF) - pref2))
            dest.setDiffpref(abs(link.getCbo(Entity.PRF) - pref2))

            #NL: ask end1
            #NL: if empty? [cboeu1] of my-out-links with [citlink? = ticks]:
            #if self.getLinksFromNode(t,orig) is None:
            #    link.setTempEu(0)
            #else:
                #NL: set temp-eu max [cboeu1] of my-out-links with [citlink? = ticks]
                # PIKE Needs to be refined for future models could have two agents one close to preference and one close to to EU
                # PIKE changed to Entity.EU from "cboeu'; 
                # PIKE changed code for getCurrentMaxOutlinks
            #print ("step 3a-2")
            val = self.getCurrentMaxOutlinks(cits, orig, Entity.EU)
            #print("\t\tsetTemp_Eu orig setting to: %s"%val)
            link.setTempEu(LINK_CITS.ORIGIDX,val)
            orig.setTemp_Eu(val)
            
            #print ('3a-2')
            #NL: set minpref min [diffpref1] of my-out-links with citlink? = ticks]
            #!!!link.setDiffpref(LINK_CITS.ORIGIDX, self.getCurrentMinOutlinks(cits, orig,"diffpref"))
            val = self.getDiffprefMinOutlinks(cits, orig)
            link.setMinpref(LINK_CITS.ORIGIDX, val)
            orig.setMinpref(val)
                                                    

            #NL: ask end2 [
            #NL: if empty? [cboeu1] of my-in-links with [citlink? = ticks]:
            #if self.getLinksFromNode(t,dest) is None:
            #    #NL: set temp-eu 0
            #    link.setTempEu(0)
            #else:
               #NL: set temp-eu max [cboeu2] of my-in-links  with [citlink? = ticks]
            #   link.setTempEu( dest.getMaxOutlinks(t,dest.getUID(),"Entity.EU") )

               #NL: set minpref min [diffpref2] of my-in-links with [citlink? = ticks]
             #  link.setMinpref( dest.getMinOutlinks(t,dest.getUID(),"diffpref") )
            
            #PIKE MADE SAME FOR desitnation node as orginal node
            #print ('3a-3')
            val = self.getCurrentMaxOutlinks(cits,dest, Entity.EU)
            link.setTempEu(LINK_CITS.DESTIDX,val)
            dest.setTemp_Eu(val)
            #print("\t\tsetTemp_Eu dest setting to: %s"%val)
            
            #print ('3a-4')
            #link.setMinpref(LINK.DESTIDX, self.getCurrentMinOutlinks(cits,dest,"diffpref"))
            val = self.getDiffprefMinOutlinks(cits, dest)
            link.setMinpref(LINK_CITS.DESTIDX,val)
            dest.setMinpref(val)
            
            #print (link.getDiffpref(LINK_CITS.ORIGIDX))
            #if link.getCboeu(LINK_CITS.ORIGIDX) < link.getDiffpref(LINK_CITS.ORIGIDX):
            #    self.linkcits[t].remove(link)

            #if cboeu1 < [own-eu] of end1 [die]
            #elif link.getCboeu(LINK_CITS.ORIGIDX) < orig.getOwn(Entity.EU):
            #    self.linkcits[t].remove(link)

            #if cboeu2 <= [own-eu] of end2 [die]
            #elif link.getCboeu(LINK_CITS.DESTIDX) < dest.getOwn(Entity.EU):
            #    self.linkcits[t].remove(link)

            #if diffpref2 > [minpref] of end2 [die]
            # PIKE - sign was backward -------------------RFI to Z seems unnecessary will always be equal based on previous method
            #elif link.getDiffpref(LINK_CITS.DESTIDX) > dest.getMinpref():
            #    self.linkcits[t].remove(link)
            count +=1
            #print (count)
                
        #print("\tEnd UpdateLinks with %s links in %s seconds"%(len(self.linkcits[t]),time.time()-starttime))

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
        #print ("\t***Starting Manage with %s links"%len(self.linkcits[t]))
        #starttime=time.time()
        for link in self.linkcits[t]:
            orig = cits.getCIT( link.getOrignode() )
            dest = cits.getCIT( link.getDestnode() )
            #print ("\t\tlink.Cboeu(orig) < orig.getTemp_Eu:\t %s < %s"%(link.getCboeu(LINK_CITS.ORIGIDX),orig.getTemp_Eu()))
            #print ("\t\tlink.Cboeu(orig) < orig.getOwn(EU):\t %s < %s"%(link.getCboeu(LINK_CITS.ORIGIDX),orig.getOwn(Entity.EU)))
            #print ("\t\tlink.Cboeu(dest) < dest.getOwn(EU):\t %s < %s"%(link.getCboeu(LINK_CITS.DESTIDX),dest.getOwn(Entity.EU)))
            #print ("\t\tlink.getDiffpref < dest.getMinpref:\t %s < %s"%(link.getDiffpref(LINK_CITS.DESTIDX),dest.getMinpref()))
            
            #if cboeu1 < [temp-eu] of end1 [die]
            if link.getCboeu(LINK_CITS.ORIGIDX) < orig.getTemp_Eu(): self.removeLink(t,cits,orig,dest)
            
            #if cboeu1 < [own-eu] of end1 [die]
            if link.getCboeu(LINK_CITS.ORIGIDX) < orig.getOwn(Entity.EU): self.removeLink(t,cits,orig,dest)

            #if cboeu2 <= [own-eu] of end2 [die]
            if link.getCboeu(LINK_CITS.DESTIDX) < dest.getOwn(Entity.EU): self.removeLink(t,cits,orig,dest)

            #if diffpref2 > [minpref] of end2 [die]
            # PIKE - sign was backward (CMP Changed it): 
            # seems unnecessary will always be equal based on previous method
            if link.getDiffpref(LINK_CITS.DESTIDX) < dest.getMinpref(): self.removeLink(t,cits,orig,dest)

            # ifelse ([temp-eu] of end1 > [own-eu] of end1) and
            #        ([temp-eu] of end2 > [own-eu] of end2)
            if (orig.getTemp_Eu() > orig.getOwn(Entity.EU)) and (dest.getTemp_Eu() > dest.getOwn(Entity.EU)):
                #ask end1 [
                #set turcbo 2
                orig.setTurcbo(2)

                #set stakeholder? 1
                orig.setStakeholder(True)
                
                #helper variable 
                
                
                maxval = self.getCurrentMaxOutlinks(cits,orig,Entity.PRF)
                #set own-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setOwn(Entity.PRF, maxval)

                #set sown-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setSown(Entity.PRF, maxval)

                #set cbo-pref max [cbopref] of my-out-links with [citlink? = ticks]
                orig.setCbo(Entity.PRF, maxval)

                #set own-power 1.5 * own-power
                orig.setOwn(Entity.POW, 1.5 * orig.getOwn(Entity.POW))

                #set sown-power max [cbopower] of my-out-links with [citlink? = ticks]
                 #PIKE update to getCurrentMaxOutLinks, other inputs
                maxval = self.getCurrentMaxOutlinks(cits,orig,Entity.POW)
                orig.setSown(Entity.POW, maxval)

                #set cbo-power max [cbopower] of my-out-links with [citlink? = ticks]
                orig.setCbo(Entity.POW, maxval)

                
                maxval = self.getCurrentMaxOutlinks(cits,orig,Entity.EU)
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
                #  PIKE---does the stakeholder calculate of other side or is this an error why would this be false??????
                dest.setStakeholder(False)

                #set own-pref [cbo-pref] of other-end
                dest.setOwn(Entity.PRF, orig.getCbo(Entity.PRF))

                #set cbo-pref [cbo-pref] of other-end
                dest.setCbo(Entity.PRF, orig.getCbo(Entity.PRF))

                #set own-power 1.5 * own-power
                dest.setOwn(Entity.POW, 1.5 * dest.getOwn(Entity.POW))

                #set cbo-power 0
                dest.setCbo(Entity.POW, 0)

                maxval = self.getCurrentMaxInlinks(cits, dest,Entity.EU)
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
                #self.linkcits[t].remove(link)
                self.removeLink(t,cits,orig,dest)
        #print ("\tEnding ManageLinks with %s links in %s seconds"%(len(self.linkcits[t]),time.time()-starttime))
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
        #print ("\t***Starting ManagePreviousLink with %s links"%len(self.linkcits[t]))
        starttime=time.time()
        #print ('previouslinks1', len(self.linkcits[t]))
        for link in self.linkcits[t]:
            #ask linkcits with [citlink? < ticks] [
            orig = cits.getCIT( link.getOrignode() )
            dest = cits.getCIT( link.getDestnode() )

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
                
                #PIKE missing set cboeu cbopower * (100 - abs (cbopref - cbopref))
                link.setCbo(Entity.EU, orig.getCbo(Entity.POW) * 100 )
                
                #################### PIKE skipped cboeu12 as not referenced later as in line 120 
                
                #if(cboeu1 < [own-eu] of end1) or (cboeu2 < [own-eu] of end2) [
                if (link.getCboeu(LINK.ORIGIDX) < orig.getOwn(Entity.EU)) or (link.getCboeu(LINK.DESTIDX) < dest.getOwn(Entity.EU)):
                    #ask end1 [
                    #if count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [

                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    #if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinksToNode(t,orig)) == 0:
                    #if len(orig.getOutlinks()) == 0 and len(orig.getInlinks()) == 0:
                    #set turcbo 1
                    orig.setTurcbo(1)

                    #set cbo-pref 0
                    orig.setCbo(Entity.PRF,0)

                    #set cbo-power 0
                    orig.setCbo(Entity.POW,0)

                    #set stakeholder? 0
                    orig.setStakeholder(False)

                    #set own-power own-power / 1.5
                    # PIKE- changed to / instead of multiplication
                    orig.setOwn(Entity.POW, orig.getOwn(Entity.POW) / 1.5)

                    #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                    orig.setOwn(Entity.EU, 100 * orig.getOwn(Entity.POW))

                    #set shape "circle"
                    orig.setShape('o')
                    #ask end2 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    #if len(self.getLinksFromNode(t,dest)) == 0 and len(self.getLinksToNode(t,dest)) == 0:
                    #if len(dest.getOutlinks()) == 0 and len(dest.getInlinks()) == 0:
                    #set turcbo 1
                    dest.setTurcbo(1)

                    #set cbo-pref 0
                    dest.setCbo(Entity.PRF,0)

                    #set cbo-power 0
                    dest.setCbo(Entity.POW,0)

                    #set stakeholder? 0
                    dest.setStakeholder(False)

                    #set own-power own-power / 1.5
                    # PIKE correct to / instead of *--loses eocnomy of scale
                    dest.setOwn(Entity.POW, dest.getOwn(Entity.POW) / 1.5)

                    #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                    dest.setOwn(Entity.EU, 100 * dest.getOwn(Entity.POW))

                    #set shape "circle"
                    dest.setShape('o')
                    #die
                    #self.linkcits[t].remove(link)
                    self.removeLink(t,cits,orig,dest)
                else:
                    #ask end1
                    #ifelse count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinksToNode(t,orig)) == 0: 
                    #if len(orig.getOutlinks()) == 0 and len(orig.getInlinks()) == 0:
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
                        orig.setStakeholder(True)

                    #ask end2 [
                    #ifelse count my-out-links with [citlink? = 2] = 0 and count my-in-links with [citlink? = 2] = 0 [
                    #!!! NOT SURE WHAT CITLINK? = 2 CONDITION IS OR WHERE IT IS SET
                    ## PIKE think this should be if there is a link?
                    if len(self.getLinksFromNode(t,dest)) == 0 and len(self.getLinksToNode(t,dest)) == 0:
                    #if len(dest.getOutlinks()) == 0 and len(dest.getInlinks()) == 0:
                        #set turcbo 2
                        dest.setTurcbo(2)

                        #set stakeholder? 0
                        dest.setStakeholder(False)

                        #set own-pref [cbo-pref] of other-end
                        dest.setOwn(Entity.PRF, orig.getCbo(Entity.PRF))

                        #set cbo-pref [cbo-pref] of other-end
                        dest.setCbo(Entity.PRF, orig.getCbo(Entity.PRF))

                        #set cbo-power 0
                        dest.setCbo(Entity.POW,0)

                        #set own-eu (100 - abs (own-pref - own-pref)) * own-power
                        dest.setOwn(Entity.EU, 100 * dest.getOwn(Entity.POW))
                    else:
                        #set stakeholder? 1
                        dest.setStakeholder(True)
                    #set hidden? FALSE
                    #self.linkcits[t].setHidden(False)
        #print ("\tEnding ManagePreviousLink with %s links in %s seconds"%(len(self.linkcits[t]),time.time()-starttime))
        
        
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
    def UpdateCITS(self,t, cits):
        #ask cits with [stakeholder? = 1] [
        starttime=time.time()
        #print("\t***Starting UpdateCITS")
        for c in cits.getCITS():
            if c.getStakeholder():
                #!!! I am not convinced the below is theoretically correct (syntactically ok). 
                #    Did he really mean to nest them this way? t2 + t3 - own * (t4 + t5 - 1)???
                #set cbo-power = (sum [cbopower] of my-out-links with [citlink? > 0]) + 
                #    (sum [cbopower] of my-in-links with [citlink? > 0]) - own-power * 
                #    ((count my-out-links with [citlink? > 0]) + (count my-in-links with [citlink? > 0]) - 1)]

                #t2 = sum [cbopower] of my-out-links with [citlink? > 0]
                #t4 = count my-out-links with [citlink? > 0]
                t2,t4 = self.getSumOutlinksP(cits, c, Entity.POW)

                #t3 = sum [cbopower] of my-in-links with [citlink? > 0]
                #t5 = count my-in-links with [citlink? > 0]
                t3,t5 = self.getSumInlinksP(cits, c, Entity.POW)

                c.setCbo(Entity.POW,(t2) + (t3) - (c.getOwn(Entity.POW)* ((t4) + (t5) - 1)))
                print("c.setCBO(POW) = %s"%((t2) + (t3) - (c.getOwn(Entity.POW)* ((t4) + (t5) - 1))))
        #print("\tEnding UpdateCITS in %s seconds"%(time.time()-starttime))

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
        for link in self.linkcits[t]:
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
        for link in self.linkcits[t]:
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
    def removeLink(self,t,cits,orig,dest):
        #print("\t***REMOVING LINK(%s,%s) len=%s"%(orig.getUID(),dest.getUID(),len(self.linkcits[t])))
        for link in self.linkcits[t]:
            if link.getOrignode() == orig.getUID() and link.getDestnode() == dest.getUID():
                self.linkcits[t].remove(link)
                
                #cits.getCIT(orig.getUID()).removeOutlink(dest.getUID())
                #cits.getCIT(orig.getUID()).setCitlink(0)  #!!! not sure this is right... but seems so
                orig.removeOutlink(dest.getUID())
                orig.setCitlink(0)  #!!! not sure this is right... but seems so
                
                #cits.getCIT(dest.getUID()).removeInlink(orig.getUID())
                #cits.getCIT(dest.getUID()).setCitlink(0)  #!!! not sure this is right... but seems so
                dest.removeInlink(orig.getUID())
                dest.setCitlink(0)  #!!! not sure this is right... but seems so
                
                break #No need to continue... link destroyed
        #print("\t***LINK REMOVED len=%s"%(len(self.linkcits[t])))
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
    def getCurrentMaxOutlinks(self, cits, node, param):
        lv = 0.0
        # Getting none error in loop moved if none = 0 down here
        for i in node.getOutlinks():
            dest = cits.getCIT(i)
            if lv < dest.getCbo(param):
                lv = dest.getCbo(param)
        return lv

    def getDiffprefMinOutlinks(self, cits, node):
        lv = 100000000.0
        # Getting none error in loop moved if none = 0 down here
        for i in node.getOutlinks():
            dest = cits.getCIT(i)
            if lv > dest.getDiffpref():
                lv = dest.getDiffpref()
        
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
    def getCurrentMaxInlinks(self, cits, node, param):
        lv = 0.0
        for i in node.getInlinks():
            dest = cits.getCIT(i)
            if dest.getCbo(param) == None:
                return 0
            elif lv < dest.getCbo(param):
                lv = dest.getCbo(param)
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
    def getCurrentMinOutlinks(self, cits, node, param):
        lv = 100000000.0
        for i in node.getOutlinks():
            dest = cits.getCIT(i)
            dval = 0
            if param == "diffpref":
                dval = dest.getDiffpref()
            else:
                dval = dest.getCbo(param) 
            
            if lv > dval:
                lv = dest.getCbo(param)
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
    def getCurrentMinInlinks(self, cits, node, param):
        lv = 100000000.0
        for i in node.getInlinks():
            dest = cits.getCIT(i)
            if dest.getCbo(param) == None:
                return 0
            elif lv > dest.getCbo(param):
                lv = dest.getCbo(param)
        return lv



    ##----------------------------------------------------------------------
    #########################################################################
    # PIKE REMOVED [t] for i in self.linkcits[t]- believe unnecessary since update need to 2check
    ###################################################################################
    
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
    def getSumOutlinksP(self, cits, node, param):
        #print("getSumOutlinksP=>",type(cits))
        lv = 0
        cnt = 0
        for i in node.getOutlinks():
            other = cits.getCIT(i)
            if other.getCitlink() > 0:
                lv += other.getCbo(param)
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
    def getSumInlinksP(self, cits, node, param):
        lv = 0
        cnt = 0
        #print("getSumInlinksP=>",type(cits))
        for i in node.getInlinks():
            other = cits.getCIT(i)
            if other.getCitlink() > 0:
                lv += other.getCbo(param)
                cnt+=1
        return lv,cnt