# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:53:34 2020

@author: takashi
"""

import numpy as np
import random
import sys
import math
from scipy.stats import binom

import utility_functions as uf

UNIVERSE = 10**100
EntropyCalc = ""

def set_Json_item(entropy = ""):
    global EntropyCalc
    EntropyCalc = entropy
    
    
class Reaction:
    
    def __init__(self, reactionName, before, reactionRate, normConst, after):
        self.reactionName = reactionName                            # Reaction name
        self.prob = float(reactionRate)                  # probability
        self.normConst = uf.convert_to_int(normConst)                    # 2023.9.9   it is int.
        self.beforeElemNum = len(before)
        self.before = before                       # [[n1, el_b1],[n2, el_b2], --- ]
        self.after = after                         # [[m1, el_a1],[m2, el_a2], --- ]
        self.p = self.prob/(1.0 + self.prob)  # 2022.8.23
        self.info = []                                             # 2022.11.19 
        self.infoAddUp = []
        self.forEntropyCalc = []
        self.entropy = []
           
    def react(self):                          # 2022.3.20
        # 2022.5.11
        elNumList = [el.getN()/order for order, el in self.before]
        flg_info = 0
        
        if len(self.before) == 1:         # 2022.3.19
            p = self.p                    # 2022.8.23
            minNK = elNumList[0]          # 2022.5.21
        elif len(self.before) >= 2:
            minNK, p = self._getProb2(self.before)           # 2022.3.15
            
        k = self._getIntK(minNK, p)
        
        # print("In def react: minNK, p, k; ", minNK, p, k)           # 2023.10.28
        
        if self._updateMulti(k, self.before, self.after) == 0:
            self._updateMulti(-k, self.before, self.after)          # 2022.11.19 
        elif k == 0:
            pass
        else:
            flg_info = 1
            
        self._set_infomation_Data(flg_info, k, minNK, p)
        

    def _set_infomation_Data(self, flg_info, k, minNK, p):
        if flg_info == 0:
            self._setInformation(0, 0, 0) 
        else:
            self._setInformation(k, minNK, p)
        self._updateInfoAddUp()                                    # 2022.11.19
        
        if EntropyCalc == "YES":
            self.forEntropyCalc.append((minNK, p))                 # 2023.3.2
        else:
            self.forEntropyCalc.append((0, 0))                     # 2023.3.2

            
    def _getProb2(self, before):                                   # 2023.10.28
        minNK = UNIVERSE
        min_el = None
        min_el_num = 0
        max_order_for_mini_el = 1
        max_order_flg = 0
        non_min = []
        p = 1
        
        for order, el in before:
            nk = int(el.getN()/order)
            if nk < minNK:
                minNK = nk
                min_el = el
        # print("minNK", minNK)                       # 2023.10.28

        for order, el in before:
            if el == min_el:
                min_el_num += 1
         
        if minNK > 0 and int(minNK/min_el_num) == 0:
            minNK = 1
        else:
            minNK = int(minNK/min_el_num)

        for order, el in before:                
                if order > max_order_for_mini_el and el == min_el:
                    max_order_for_mini_el = order
                    
        for order, el in before:
                if order == max_order_for_mini_el and el == min_el and max_order_flg == 0: 
                    max_order_flg = 1
                else:
                    non_min.append([order, el])  
                    
        # print("minNK", minNK)                                                  # 2023.10.28
        # print("min_el_num, max order : ", min_el_num, max_order_for_mini_el)        
                
        for order, el in non_min:
            prob = self.prob*(el.getN()/order)/self.normConst
            p *= prob/(1.0 + prob)
            
        return minNK, p

    def _getIntK(self, n, p):
        # eandom.gauss is used for large int 
        if n > int(1e15) :
            k = random.gauss(n*p, (n*p*(1-p))**0.5)
        else:
            k = np.random.binomial(n, p)
        return int(k)

    def _updateMulti(self, k, before, after):
        flg = 1
        for order, el in before:
            el.decrease(order*k)
            flg *= 0 if (el.getN() < 0 and k > 0) else 1
        for order, el in after:
            el.increase(order*k)   
        return flg
    
    # 2022.11.19
    def _setInformation(self, k, N, p):
        try:                                #  2023.3.25
            bi_pmf = binom.pmf(k, N, p)
        except:
            bi_pmf = 0.0
            self.info.append(0)
        
        if p == 0 or bi_pmf == 0.0:
            self.info.append(0)
        else:
            try:
                self.info.append(-math.log2(binom.pmf(k, N, p)))       # 2022.12.1  
            except:
                self.info.append(0)
            
    def _updateInfoAddUp(self):
        try:
            nextValue = self.infoAddUp[-1] + self.info[-1]
        except:
            nextValue = self.info[0]
        self.infoAddUp.append(nextValue)
        

# 2022.6.25  2023.9.19
class ReactionR1_plus(Reaction):
    
    def __init__(self, reactionName, before, reactionRate, normConst, after):
        super().__init__(reactionName, before, reactionRate, normConst, after)
        
    def react(self):    
        k = super()._getIntK(1, self.p)                        # 2022.12.21
        super()._updateMulti(k, self.before, self.after)    
        super()._set_infomation_Data(0, k, 1, self.p)
        

# 2022.8.23  2023.9.19
class ReactionR1_minus(Reaction):
    
    def __init__(self, reactionName, before, reactionRate, normConst, after):
        super().__init__(reactionName, before, reactionRate, normConst, after)
        
    def react(self):    
        k = super()._getIntK(1, self.p)                       # 2022.12.21  
        if super()._updateMulti(k, self.before, self.after) == 0:
            super().before[0][1].decrease(self.before[0][1].getN())
        
        super()._set_infomation_Data(0, k, 1, self.p)        
        

# 2023.9.18
class Reaction_AddSub(Reaction):

    def __init__(self, reactionName, before, after):
        super().__init__(reactionName, before, 0, 0, after)   
        
        if len(self.after) > 1:
            print("At react in Reaction_Add class")
            sys.exit("After element must be one.")   
         
    def react(self):
        sumOfthem = 0
        for order, el in self.before:
            el_n = order*el.getN()
            sumOfthem += el_n        
        self.after[0][1].n = sumOfthem 
        
        super()._set_infomation_Data( 0, 0, 1, self.p)      
        
            
class reactions:
    
    def __init__(self): 
        self.reactions = {}
        self.independent_Reaction_sets = []                      # 2023.5.28
        
    def setReaction(self, ls, elements, normConst):
        className = ls[0].strip()
        reactionName = className + '_' + ls[1].strip()
        self._checkReactionName(reactionName)
        
        if   className == "r1_+" or className == "R1_+":
            after = self._makeList(ls[5:7], elements)
            self.reactions[reactionName] = ReactionR1_plus(reactionName, [], ls[4], normConst, after)

        elif   className == "r1_-" or className == "R1_-":
            before = self._makeList(ls[2:4], elements)
            self.reactions[reactionName] = ReactionR1_minus(reactionName, before, ls[4], normConst, [])

        elif   className == "r1_0" or className == "R1_0":
            before = self._makeList(ls[2:4], elements)
            self.reactions[reactionName] = Reaction(reactionName, before, ls[4], normConst, [])
            
        elif className == "r1_1" or className == "R1_1":
            self._defineReaction(elements, 2, 4, 5, 7, ls, reactionName, normConst)
            
        elif className == "r1_2" or className == "R1_2":
            self._defineReaction(elements, 2, 4, 5, 9, ls, reactionName, normConst)
            
        elif className == "r1_3" or className == "R1_3":
            self._defineReaction(elements, 2, 4, 5, 11, ls, reactionName, normConst)
            
        elif className == "r1_4" or className == "R1_4":
            self._defineReaction(elements, 2, 4, 5, 13, ls, reactionName, normConst)
            
        elif className == "r2_1" or className == "R2_1":
            self._defineReaction(elements, 2, 6, 7, 9, ls, reactionName, normConst)
            
        elif className == "r2_2" or className == "R2_2":
            self._defineReaction(elements, 2, 6, 7, 11, ls, reactionName, normConst)
            
        elif className == "r2_3" or className == "R2_3":
            self._defineReaction(elements, 2, 6, 7, 13, ls, reactionName, normConst)

        elif className == "r3_1" or className == "R3_1":
            self._defineReaction(elements, 2, 8, 9, 11, ls, reactionName, normConst)
            
        elif className == "r3_2" or className == "R3_2":
            self._defineReaction(elements, 2, 8, 9, 13, ls, reactionName, normConst)
            
        elif className == "r3_3" or className == "R3_3":
            self._defineReaction(elements, 2, 8, 9, 15, ls, reactionName, normConst)
            
        elif   className == "r+-=" or className == "R+-=":
            before = self._makeList(ls[2:4], elements)
            length = len(ls)
            before = self._makeList_02(ls[2:length-2], elements)
            after = [ [ 1, elements[ ls[-1] ] ] ]
            self.reactions[reactionName] = Reaction_AddSub(reactionName, before, after)

    # The main code, binomial_xxx.py use this method.
    # The reactionManage_02.py also use this.    
    def setReactionMulti(self, ls1, reactionRate, normConst, ls3, elements):
        reactionName = ls1[0].strip() + '_' + ls1[1].strip()
        self._checkReactionName(reactionName)
        self._check_reactionRate(float(reactionRate))
        self._check_normConst(float(normConst))   
        before = self._makeList(ls1[2:], elements)        
        after = self._makeList(ls3, elements)
        self.reactions[reactionName] = Reaction(reactionName, before, reactionRate, normConst, after)

        
    def _makeList_02(self, ls_b, elements):
        elems = []
        itit = iter(ls_b)
        for coeff, element in zip(itit, itit):
            elems.append([uf.convert_to_int(coeff), elements[element]])  
        return elems
                
    def _checkReactionName(self, reactionName):
        if reactionName in self.reactions.keys():
            print(f"Same reaction {reactionName} is defined!")
            sys.exit("Chack the reaction name in *Reaction.")
            
    def _check_normConst(self, normConst):
        if float(normConst) <= 0:
            print("At *Reaction definition stage: ")
            sys.exit("Error: Normalized constant is under ZERO. It munst be larger than ZERO.")  
        
    def _check_reactionRate(self, reactionRate):
        if float(reactionRate) <= 0:
            print("At *Reaction definition stage: ")
            sys.exit("Error: Reaction rate is under ZERO. It munst be larger than ZERO.")   

    def _defineReaction(self, elements, b1, b2, a1, a2, ls, reactionName, normConst):
        before = self._makeList(ls[b1:b2], elements)
        after = self._makeList(ls[a1:a2], elements)       
        all_len = len(before)*2 + len(after)*2 + 3
        if all_len == len(ls) and len(ls) == a2:                             # 2023.5.7
            pass
        elif ls[-1] == "":                                                   # 2023.5.6
            ls.pop(-1)
        else:
            print(f"{ls[0]}_{ls[1]} definition was wrong.")
            sys.exit(f"The number of terms needs {a2} characters")
        
        self._check_normConst(normConst)    
        self._check_reactionRate(float(ls[b2]))
        self.reactions[reactionName] = Reaction(reactionName, before, ls[b2], normConst, after)            
        
    def _makeList(self, ls_x, elements):
        elems = []
        itit = iter(ls_x)
        for order, element in zip(itit, itit):
            if float(order) <= 0:
                print("At *Reaction definition stage: ")
                sys.exit("Error: Order Constant is under ZERO. It munst be larger than ZERO.")
            elems.append([uf.convert_to_int(order), elements[element]])  
        return elems

    
    def createReactionPolymer(self, ls, all_elements, normConst):
        # if ls[3] == "M=*_R" and ls[5] == "M":
        if ls[0] == "rP_elong":
            for el, el_obj in all_elements.elements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees + int(ls[4])
                    after = self._getAfterPolymer("M=*_R", deg, all_elements)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(el_obj.degrees), ls[2], el, ls[4], ls[5]]
                        ls2 = [ls[6], normConst]
                        ls3 = [ls[7], after]
                        # all_reactions.setReactionMulti(ls1, ls2, ls3, all_elements.elements) 
                        self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements) 
        # elif ls[3] == "M=*_R" and ls[5] == "M=*_R":
        elif ls[0] == "rP_termi":
            for el_1, el_obj_1 in all_elements.polymers.items():
                deg_1 = el_obj_1.degrees
                for el_2, el_obj_2 in all_elements.polymers.items():
                    deg_2 = el_obj_2.degrees
                    if el_obj_1.type == "M=*_R" and el_obj_2.type == "M=*_R" and deg_1 <= deg_2:
                         deg = deg_1 + deg_2
                         after = self._getAfterPolymer("M=*", deg, all_elements)
                         if after != "":
                             ls1 = ["r2_1", ls[1]+"_"+str(deg_1) + "+" + str(deg_2), ls[2], el_1, ls[4], el_2]
                             ls2 = [ls[6], normConst]
                             ls3 = [ls[7], after]
                             # all_reactions.setReactionMulti(ls1, ls2, ls3, all_elements.polymers)  
                             self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.polymers) 
        elif ls[0] == "rP_trans":
            print("in rP_trans")
            for el, el_obj in all_elements.elements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees
                    after = self._getAfterPolymer("M=*", deg, all_elements)
                    print("after element: ", after)
                    if after != "":
                        ls1 = ["r3_3", ls[1]+"_"+str(deg), ls[2], el, ls[4], ls[5], ls[6], ls[7]]
                        ls2 = [ls[8], normConst]
                        ls3 = [ls[9], after, ls[11], ls[12], ls[13], ls[14]]
                        print(ls1, ls2, ls3)
                        # all_reactions.setReactionMulti(ls1, ls2, ls3, all_elements.elements)
                        self.setReactionMulti(ls1, ls[8], normConst, ls3, all_elements.elements)
        else:
            # This code should go to Polymer class.
            print()
            print("***  Error  ***")
            print("Use \"M\" for monomer in Polymerization process!!")
            sys.exit()
                             
    def _getAfterPolymer(self, pType, deg, all_elements):
        rName = ""
        for el, el_obj in all_elements.polymers.items():
            if el_obj.type == pType and el_obj.degrees == deg:
                rName = el
        return rName    

    # under constraction 2023.5.28
    def separate_independent_reactions(self):
        reactionsName_elements = {}
        for rm in self.reactions.values():
            reactionName = rm.reactionName
            elementNames = self._extract_inner_elements(rm.before, rm.after) 
            reactionsName_elements[reactionName] = elementNames
            print(reactionName, elementNames)
        self.independent_Reaction_sets = self._make_independent_reaction_Sets(reactionsName_elements)

    def _extract_inner_elements(self, before, after):
        beforeNames = [el[1].name for el in before]
        afterNames = [el[1].name for el in after]
        return beforeNames + afterNames

    def _make_independent_reaction_Sets(self, reactions):
        independent_reaction_Sets = []
        remaining_reactions = dict(reactions)
        step = 1
        while remaining_reactions:
            selected_reactions = self._select_reactions(remaining_reactions)
            remaining_reactions = {
                reaction: elements
                for reaction, elements in remaining_reactions.items()
                if reaction not in selected_reactions
            }
            independent_reaction_Sets.append(selected_reactions)
            print("!!! !!! !!! !!! !!!")
            print(f"Step {step}: Selected Reactions:", selected_reactions)
            step += 1
        print("Independent_reaction_Sets:", independent_reaction_Sets)
        return independent_reaction_Sets

    def _select_reactions(self, reactions):
        selected_reactions = []
        for reaction, elements in reactions.items():
            can_select = True
            for reac in selected_reactions:
                if any(element in reactions[reac] for element in elements):
                    can_select = False
                    break
            if can_select:
                selected_reactions.append(reaction)
        return selected_reactions
