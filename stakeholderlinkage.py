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
from link_stakeholders import *
from cits import *

##############################################################################
##############################################################################
# CLASS::StakeholderLinkage
#
# Purpose: Implements the maintenance of the array/collection of Stakeholder 
#          Links
#
class StakeholderLinkage:
  
    ########################################################################
    ## Standard initialization routine
    def __init__(self,max_t):
        self.linkshldrs = {}
       
    ##----------------------------------------------------------------------
    ## Name: FormLinks
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) cits: the array of cits
    ##
    ## Returns: Nothing
    def FormLinks(self,t,cits):
        links = []
        
        for ci in cits.cits:
            #check if ci is stakeholder
            
            ret = cits.stakeholder_group(ci)
            
            for l in range(len(ret)):
               
               #add to self.linkcits
               links.append(LINK_STAKEHOLDERS(ci.UID,ret[l]))
               links[l].setHidden(True)
               #append to other citizens outlinks
               #ret[l].setInlinks(LINK_CITS(ci.UID, ret[l]))
                            
            
        self.linkshldrs[t] = links
        print ('FORM Stake LINKS:', len(self.linkshldrs[t]))
            
      
                       
        
    
    ##----------------------------------------------------------------------
    ## Name: UpdateSHolderLinks
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) cits: the array of cits
    ##
    ## Returns: Nothing
    ## PIKE added t to parameters
    def UpdateSHolderLinks(self,t,cits):
        #ask cits with [stakeholder? = 1] [
        #  create-linkstakeholders-to cits with [stakeholder? = 1] with [who != [who] of myself]
        #  [
        for link in self.linkshldrs[t]:
            #For readability, get origin and destination node of the link
            orig = cits.getCIT( link.getOrignode() )
            dest = cits.getCIT( link.getDestnode() )

            # set cbolink? ticks
            # PIKE changed form True to t
            link.setCbolink(t)

            # set spref1 [sown-pref] of end1
            spref1 = orig.getSown(Entity.PRF)

            # set spower1 [sown-power] of end1
            spower1 = orig.getSown(Entity.POW)

            # set seu1 [sown-eu] of end1
            seu1 = orig.getSown(Entity.EU)

            # set spref2 [sown-pref] of end2
            spref2 = dest.getSown(Entity.PRF)

            # set spower2 [sown-power] of end2
            spower2= dest.getSown(Entity.POW)

            # set seu2 [sown-eu] of end2
            seu2= dest.getSown(Entity.EU)

            # set scbopref ((spref1 * spower1 + spref2 * spower2)/(spower1 + spower2 + 0.0000001))
            link.setScbo(Entity.PRF, ((spref1 * spower1 + spref2 * spower2)/(spower1 + spower2 + 0.0000001)))

            # set scbopower spower1 + spower2
            link.setScbo(Entity.POW, spower1 + spower2)

            #!!!set scboeu scbopower * (100 - abs (scbopref - scbopref))
            link.setScbo(Entity.EU, link.getScbo(Entity.POW) * 100 )

            # set scboeu1 (100 - abs(scbopref - spref1)) * (spower1 + (scbopower - spower1) * (spower1 / (scbopower + 0.000001)))
            link.setScboeu(LINK.ORIGIDX, (100 - abs(link.getScbo(Entity.PRF) - spref1)) * (spower1 + (link.getScbo(Entity.POW) - spower1) * (spower1 / (link.getScbo(Entity.POW) + 0.000001))))

            # set scboeu2 (100 - abs(scbopref - spref2)) * (spower2 + (scbopower - spower2) * (spower2 / (scbopower + 0.000001)))
            link.setScboeu(LINK.DESTIDX, (100 - abs(link.getScbo(Entity.PRF) - spref2)) * (spower2 + (link.getScbo(Entity.POW) - spower2) * (spower2 / (link.getScbo(Entity.POW) + 0.000001))))


            #ask end1 [
            #if empty? [scboeu1] of my-out-links with [cbolink? = 3][
        
            
            if self.getLinksFromNode(t,orig) is None:
                # set stemp-eu 0
                orig.setStemp_Eu(0)
            else:
                # NL: set stemp-eu max [scboeu1] of my-out-links with [cbolink? = 3]
                
                orig.setStemp_Eu( self.getCurrentMaxOutlinks(t,orig.getUID(),Entity.EU) )
             
            #ask end2 [
            #if empty? [scboeu1] of my-in-links with [cbolink? = 3][
            if self.getLinksToNode(t,dest) is None:
                # set stemp-eu 0
                dest.setStemp_Eu(0)
            else:
                # NL: set stemp-eu max [scboeu1] of my-out-links with [cbolink? = 3]
                dest.setStemp_Eu( self.getCurrentMaxOutlinks(t,dest.getUID(), Entity.EU) )
            #set hidden? TRUE
            #link.setTempEu(LINK_CITS.ORIGIDX, self.getCurrentMaxOutlinks(t,orig.getOutlinks(), Entity.EU))
            #link.setStemp(LINK_STAKEHOLDERS.ORIGIDX, self.getCurrentMaxOutlinks(t,orig.getOutlinks(), Entity.EU))
            
                       
            #link.setStemp(LINK_STAKEHOLDERS.DESTIDX, self.getCurrentMaxOutlinks(t,dest.getOutlinks(), Entity.EU))
                         
            
            
            link.setHidden(True)
        #]//End ask cits

    ##----------------------------------------------------------------------
    ## Name: ManageCurrentLink
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) cits: the array of cits
    ##
    ## Returns: Nothing
    #  ask linkcits with [citlink? = ticks] [
    def ManageCurrentLink(self,t,cits):
        #ask linkstakeholders with [cbolink? = ticks] [

        #changes to linksholders from link cits
        
        for link in self.linkshldrs[t]:
            orig = cits.getCIT( link.getOrignode() )
            dest = cits.getCIT( link.getDestnode() )

            #if ([stemp-eu] of end1) + ([stemp-eu] of end2) != (scboeu1 + scboeu2) [
            if orig.getStemp_Eu() +  dest.getStemp_Eu() != (link.getScboeu(LINK.ORIGIDX) + link.getScboeu(LINK.DESTIDX)):
                #  die
                self.removeLink(t,orig,dest)

            #if ([stemp-eu] of end1 > [sown-eu] of end1) and ([stemp-eu] of end2 > [sown-eu] of end2)
            #print ("1 node STEMP EU", orig.getStemp_Eu() )
            #print ("1 node getSown", orig.getSown(Entity.EU))
            
            
            
            if orig.getStemp_Eu() > orig.getSown(Entity.EU) and dest.getStemp_Eu() > dest.getSown(Entity.EU):
                #ask end1 [
                #set sturcbo? 1
                print ("STURCBO IS TRUE")
                orig.setSturcbo(1)

                #!!! IS THIS CORRECT???
                # PIKE Should be you are getting the max scbo preference of your outlinks as the code is only set to make one link a tick 
                maxval = self.getCurrentMaxOutlinks(t, orig.getUID(),Entity.PRF)
                #set sown-pref max [scbopref] of my-out-links with [cbolink? = ticks]
                orig.setSown(Entity.PRF, maxval)
                
                orig.setown(Entity.PRF, maxval)
                
                orig.setScbo(Entity.PRF, maxval)
                
               
                maxval = self.getCurrentMaxOutlinks(t, orig.getUID(),Entity.POW)
                #set scbo-power max [scbopower] of my-out-links with [cbolink? = ticks]
                orig.setScbo(Entity.POW, maxval)

                maxval = self.getMaxOutlinks(t, orig.getUID(),Entity.EU)
                #set sown-eu max [scboeu1] of my-out-links with [cbolink? = ticks]
                orig.setSown(Entity.EU, maxval)
                
                orig.setScbo(Entity.EU, maxval)

                

                #ask end2 [
                #set sturcbo? 0
                dest.setSturcbo(LINK.DESTIDX,0)

                #set sown-pref [scbo-pref] of other-end
                dest.setSown(Entity.PRF, orig.getCbo(Entity.PRF))

                #set own-pref sown-pref
                dest.setOwn(Entity.PRF, link.getSown(Entity.PRF))

                #set scbo-pref [scbo-pref] of other-end
                dest.setScbo(Entity.PRF, orig.getCbo(Entity.PRF))

                #set scbo-power 0
                dest.setScbo(Entity.POW,0)

                maxval = self.getCurrentMaxOutlinks(t, dest.getUID(),Entity.EU)
                #set sown-eu max [scboeu2] of my-in-links with [cbolink? = ticks]
                dest.setSown(Entity.EU, maxval)

                #set scbo-eu max [scboeu2] of my-in-links with [cbolink? = ticks]
                dest.setScbo(Entity.EU, maxval)

                #//LINKS
                #set hidden? FALSE
                link.setHidden(False)
                #set color pink
                link.setColor("#880000")
            else:
                #ask end1 [
                #!!! WHY set 1 = 1?
                #set sown-pref sown-pref

                #set own-pref sown-pref
                orig.setSown(Entity.PRF, orig.getSown(Entity.PRF))
                orig.setSown(Entity.POW, orig.getSown(Entity.POW))
                orig.setSown(Entity.EU, orig.getSown(Entity.EU))

                #!!! WHY set 1 = 1?
                #set sown-power sown-power

                #ask end2 [
                #set sown-pref sown-pref
                #set own-pref sown-pref
                dest.setSown(Entity.PRF, dest.getSown(Entity.PRF))
                dest.setSown(Entity.POW, dest.getSown(Entity.POW))
                dest.setSown(Entity.EU, dest.getSown(Entity.EU))
                #set sown-power sown-power

    ##----------------------------------------------------------------------
    ## Name: ManagePreviousLink
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) cits: the array of cits
    ##
    ## Returns: Nothing
    # ask linkcits with [citlink? < ticks] [
    def ManagePreviousLink(self, t, cits):
        #----------
        #ask linkstakeholders with [cbolink? < ticks] [
        #chagnes to linksholders
        for link in self.linkshldrs[t]:
        #ask linkcits with [citlink? < ticks] [
            orig = cits.getCIT( link.getOrignode() )
            dest = cits.getCIT( link.getDestnode() )

            #set spref1 [sown-pref] of end1
            spref1 = orig.getSown(Entity.PRF)
            #set spower1 [sown-power] of end1
            spower1 = orig.getSown(Entity.POW)
            #set seu1 [sown-eu] of end1
            seu1 = orig.getSown(Entity.EU)

            #set spref2 [sown-pref] of end2
            spref2 = dest.getSown(Entity.PRF)
            #set spower2 [sown-power] of end2
            spower2 = dest.getSown(Entity.POW)
            #set seu2 [sown-eu] of end2
            seu2 = dest.getSown(Entity.EU)

            #set scbopref ((spref1 * spower1 + spref2 * spower2)/(spower1 + spower2 + 0.0000001))
            link.setScbo(Entity.PRF, ((spref1 * spower1 + spref2 * spower2)/(spower1 + spower2 + 0.0000001)) )

            #set scbopower spower1 + spower2
            link.setScbo(Entity.POW, spower1 + spower2 )

            #;;set scboeu scbopower * (100 - abs (scbopref - scbopref))
            link.setScbo(Entity.EU, (spower1 + spower2) * 100)

            #!!! Possible Nesting Errors: (100 - ABS(X1-X2)) * (Y1 + (Y - Y1) * (Y1 / (Y + 0...1)))
            #set scboeu1 (100 - abs(scbopref - spref1)) * (spower1 + (scbopower - spower1) * (spower1 / (scbopower + 0.000001)))
            link.setScboeu(LINK.ORIGIDX, (100 - abs(link.getScbo(Entity.PRF) - spref1)) * (spower1 + (link.getScbo(Entity.POW) - spower1) * (spower1 / (link.getScbo(Entity.POW) + 0.000001))))

            #!!! Possible Nesting Errors: (100 - ABS(X1-X2)) * (Y1 + (Y - Y1) * (Y1 / (Y + 0...1)))
            #set scboeu2 (100 - abs(scbopref - spref2)) * (spower2 + (scbopower - spower2) * (spower2 / (scbopower + 0.000001)))
            link.setScboeu(LINK.DESTIDX, (100 - abs(link.getScbo(Entity.PRF) - spref2)) * (spower2 + (link.getScbo(Entity.POW) - spower2) * (spower2 / (link.getScbo(Entity.POW) + 0.000001))))

            #if (scboeu1 < [sown-eu] of end1) or (scboeu2 < [sown-eu] of end2)
            if link.getScboeu(LINK.ORIGIDX) < orig.getSown(Entity.EU) or link.getScboeu(LINK.DESTIDX) < dest.getSown(Entity.EU):
                ##ask end1 [
                #if count my-out-links with [cbolink? = 3] = 0 and count my-in-links with [cbolink? = ticks] = 0 [
                if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinksToNode(t,orig)) == 0:
                    #set sturcbo? 0
                    orig.setSturcbo(0)
                    #set scbo-power 0
                    orig.setScbo(Entity.POW)
                #ask end2 [
                #if count my-out-links with [cbolink? = 3] = 0 and count my-in-links with [cbolink? = ticks] = 0 [
                if len(self.getLinksFromNode(t,dest)) == 0 and len(self.getLinksToNode(t,dest)) == 0:
                    #set sturcbo? 0
                    dest.setSturcbo(0)
                    #set scbo-power 0
                    dest.setScbo(Entity.POW)
                #die
                link.removeLink(t,orig,dest)
            else:
                #if [sown-pref] of end1 != [sown-pref] of end2 [
                if orig.getSown(Entity.PRF) != dest.getSown(Entity.PRF):
                        #ask end1 [
                        #if count my-out-links with [cbolink? = ticks] = 0 and count my-in-links with [cbolink? = ticks] = 0 [
                        if len(self.getLinksFromNode(t,orig)) == 0 and len(self.getLinksToNode(t,orig)) == 0:
                            #set sturcbo? 1
                            orig.setSturcbo(1)
                            
                            #get sown-pref [scbo-pref] of other-end
                            orig.setSown(Entity.PRF, dest.getScbo(Entity.PRF))
                            
                            #set scbo-pref [scbo-pref] of other-end
                            orig.setScbo(Entity.PRF, dest.getScbo(Entity.PRF))
                            
                            #set scbo-power 0
                            orig.setScbo(Entity.POW,0)
                            
                            #set sown-eu (100 - abs (sown-pref - sown-pref)) * sown-power]]
                            orig.setSown(Entity.EU, 100*orig.getSown(Entity.POW))
                        
                        #ask end2 [
                        #if count my-out-links with [cbolink? = ticks] = 0 and count my-in-links with [cbolink? = ticks] = 0 [
                        if len(self.getLinksFromNode(t,dest)()) == 0 and len(self.getLinksToNode(t,dest)) == 0:
                            #set sturcbo? 1
                            dest.setSturcbo(1)
                            
                            #set sown-pref [scbo-pref] of other-end
                            dest.setSown(Entity.PRF, orig.getScbo(Entity.PRF))
                            
                            #set scbo-pref [scbo-pref] of other-end
                            dest.setScbo(Entity.PRF, orig.getScbo(Entity.PRF))
                            
                            #set scbo power 0
                            dest.setScbo(Entity.POW,0)
                            
                            #set sown-eu (100 - abs (sown-pref - sown-pref)) * sown-power]]
                            dest.setSown(Entity.EU, 100 * dest.getSown(Entity.POW))

    ##----------------------------------------------------------------------
    ## Name: UpdateSholdrCITS
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) cits: the array of cits
    ##
    ## Returns: Nothing
    def UpdateSholdrCITS(self,t, cits):
        #-----------------
        #ask cits ...
        for c in cits:
            #... with [stakeholder? = 1] [
            if c.getStakeholder():
            #set scbo-power ( sum [scbopower] of my-out-links with [cbolink? > 0]) +
            #                 (sum [scbopower] of my-in-links with [cbolink? > 0]) -
            #                  sown-power * ((count my-out-links with [cbolink? > 0]) +
            #                  (count my-in-links with [cbolink? > 0]) - 1)]
            #
            #ask cits with [stakeholder? = 1] [ if (count my-out-links with [cbolink? >= 1] = 0) and (count my-in-links with [cbolink? >= 1] = 0)
                ## PIKE UPDATED NEEDS PROOF
                if len(c.getOutlinks()) == 0 and len(c.getInlinks()) == 0:
                    #set sturcbo? 0
                    c.sturcbo = False
                    
                    #set scbo-power 0
                    c.setScbo(Entity.POW, 0)
        #end

    ##----------------------------------------------------------------------
    ## Name: getLinksToNode
    ##
    ## Desc: Find all in-coming links to a node
    ##
    ## Paramters:
    ##    1) t: time
    ##    2) node: agent UID
    ##
    ## Returns: array of agent UIDs 
    def getLinksToNode(self,t,node):
        ret = []
        for link in self.linkshldrs[t]:
            if node == link.getDestnode():
                ret.append(link.getOrignode())
        return ret

    ##----------------------------------------------------------------------
    ## Name: getLinksToNode
    ##
    ## Desc: Find all out-going links from a node
    ##
    ## Paramters:
    ##    1) t: time
    ##    2) node: agent UID
    ##
    ## Returns: array of agent UIDs 
    def getLinksFromNode(self,t,node):
        ret = []
        for link in self.linkshldrs[t]:
            if node == link.getOrignode():
                ret.append(link.getDestnode())
        return ret

    ##----------------------------------------------------------------------
    ## Name: removeLink
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) orig: originator node UID
    ##    3) dest: destination node UID
    ##
    ## Returns: Nothing
    def removeLink(self,t,orig,dest):
        self.linkshldrs[t][orig].remove(dest)

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) node:
    ##    3) param:
    ##
    ## Returns: Nothing
    def getCurrentMaxOutlinks(self, t, node, param):
        lv = 0.0
        for i in self.linkshldrs[t]:
            if i.getOrignode() == node and lv < i.getScbo(param):
                    lv = i.getCbo(param)
        return lv

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) node:
    ##    3) param:
    ##
    ## Returns: Nothing
    def getCurrentMaxInlinks(self, t, node, param):
        lv = 0.0
        for i in self.linkshldrs[t]:
            if i.getDestnode() == node and lv < i.getScbo(param):
                lv = i.getCbo(param)
        return lv

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) node:
    ##    3) param:
    ##
    ## Returns: Nothing
    def getCurrentMinOutlinks(self, t, node, param):
        lv = 100000000.0
        for i in self.linkshldrs[t]:
            if i.getOrignode() == node and lv > i.getScbo(param):
                    lv = i.getCbo(param)
        return lv

    ##----------------------------------------------------------------------
    ## Name:
    ##
    ## Desc:
    ##
    ## Paramters:
    ##    1) t: time in ticks
    ##    2) node:
    ##    3) param:
    ##
    ## Returns: Nothing
    def getCurrentMinInlinks(self, t, node, param):
        lv = 100000000.0
        for i in self.linkshldrs[t]:
            if i.getDestnode() == node and lv > i.getScbo(param):
                lv = i.getCbo(param)
        return lv