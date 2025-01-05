#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 11:35:34 2021

@author: takashi
"""
import sys
# import random
# import collections

class createReaction:
    
    def __init__(self):
        self.allreactionATT = []     
    
    def createReactionPolymer(self, ls, elms, all_reactions):
        # if ls[3] == "M=*_R" and ls[5] == "M":
        if ls[0] == "rP_elong":
            for el, el_obj in elms.allElements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees + int(ls[4])
                    after = self._getAfterPolymer("M=*_R", deg, elms)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(el_obj.degrees), ls[2], el, ls[4], ls[5]]
                        ls2 = [ls[6], all_reactions.all]
                        ls3 = [ls[7], after]
                        # all_reactions.setReactionMulti(ls1, ls2, ls3, elms.allElements) 
                        all_reactions.setReactionMulti(ls1, ls[6], all_reactions.all, ls3, elms.allElements) 
        # elif ls[3] == "M=*_R" and ls[5] == "M=*_R":
        elif ls[0] == "rP_termi":
            for el_1, el_obj_1 in elms.polymers.items():
                deg_1 = el_obj_1.degrees
                for el_2, el_obj_2 in elms.polymers.items():
                    deg_2 = el_obj_2.degrees
                    if el_obj_1.type == "M=*_R" and el_obj_2.type == "M=*_R" and deg_1 <= deg_2:
                         deg = deg_1 + deg_2
                         after = self._getAfterPolymer("M=*", deg, elms)
                         if after != "":
                             ls1 = ["r2_1", ls[1]+"_"+str(deg_1) + "+" + str(deg_2), ls[2], el_1, ls[4], el_2]
                             ls2 = [ls[6], all_reactions.all]
                             ls3 = [ls[7], after]
                             # all_reactions.setReactionMulti(ls1, ls2, ls3, elms.polymers)  
                             all_reactions.setReactionMulti(ls1, ls[6], all_reactions.all, ls3, elms.polymers) 
        elif ls[0] == "rP_trans":
            print("in rP_trans")
            for el, el_obj in elms.allElements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees
                    after = self._getAfterPolymer("M=*", deg, elms)
                    print("after element: ", after)
                    if after != "":
                        ls1 = ["r3_3", ls[1]+"_"+str(deg), ls[2], el, ls[4], ls[5], ls[6], ls[7]]
                        ls2 = [ls[8], all_reactions.all]
                        ls3 = [ls[9], after, ls[11], ls[12], ls[13], ls[14]]
                        print(ls1, ls2, ls3)
                        # all_reactions.setReactionMulti(ls1, ls2, ls3, elms.allElements)
                        all_reactions.setReactionMulti(ls1, ls[8], all_reactions.all, ls3, elms.allElements)
        else:
            # This code should go to Polymer class.
            print()
            print("***  Error  ***")
            print("Use \"M\" for monomer in Polymerization process!!")
            sys.exit()
                             
    def _getAfterPolymer(self, pType, deg, elms):
        rName = ""
        for el, el_obj in elms.polymers.items():
            if el_obj.type == pType and el_obj.degrees == deg:
                rName = el
        return rName
