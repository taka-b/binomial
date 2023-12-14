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
import json

UNIVERSE = 10**100

f = open('binomial_parameters.json', 'r')
json_dict = json.load(f)
EntropyCalc = json_dict["EntropyCalc"]

    
class ReactionMulti:
    
    def __init__(self, rn, before, ls2, after):
        self.rName = rn                            # Reaction name
        self.prob = float(ls2[0])                  # probability
        self.all = int(float(ls2[1]))              # Reaction area        
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
        
        if len(self.before) == 1:         # 2022.3.19
            p = self.p                    # 2022.8.23
            minNK = elNumList[0]          # 2022.5.21
        elif len(self.before) >= 2:
            minNK, p = self._getProb2(self.before)           # 2022.3.15
            
        k = self._getIntK(minNK, p)
        
        if self._updateMulti(k, self.before, self.after) == 0:
            self._updateMulti(-k, self.before, self.after)         # 2022.4.30 
            self._setInformation(0, 0, 0)                          # 2022.11.19 
        elif k == 0:
            self._setInformation(0, 0, 0) 
        else:
            self._setInformation(k, minNK, p) 
        self._updateInfoAddUp()                                    # 2022.11.19
        
        if EntropyCalc == "YES":
            self.forEntropyCalc.append((minNK, p))            # 2023.3.2
        else:
            self.forEntropyCalc.append((0, 0))               # 2023.3.2
            
    def _getProb2(self, before):    # for r3-Reaction 2022.3.19　--> 4.18　--> 4.30
        minNK = UNIVERSE
        min_el = None
        non_min = []
        p = 1
        for order, el in before:
            nk = int(el.getN()/order)
            if nk < minNK:
                minNK = nk
                min_el = el
        for order, el in before:
            if el == min_el:
                pass
            else:
                non_min.append([order, el])
        for order, el in non_min:
            prob = self.prob*(el.getN()/order)/self.all
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


# 2022.6.25
class ReactionR0_1(ReactionMulti):
    
    def __init__(self, rn, before, ls2, after):
        super().__init__(rn, before, ls2, after)
        
    def react(self):    
        k = super()._getIntK(1, self.p)                       # 2022.12.21
        super()._updateMulti(k, self.before, self.after)
        self._setInformation(0, 0, 0)                         # 2022.12.21
        self._updateInfoAddUp()                               # 2022.12.21
        if EntropyCalc == "YES":
            self.forEntropyCalc.append((1, self.p))            # 2023.3.8
        else:
            self.forEntropyCalc.append((0, 0))                 # 2023.3.8

# 2022.8.23
class ReactionR0_0(ReactionMulti):
    
    def __init__(self, rn, before, ls2, after):
        super().__init__(rn, before, ls2, after)
        
    def react(self):    
        k = super()._getIntK(1, self.p)                       # 2022.12.21  
        if self._updateMulti(k, self.before, self.after) == 0:
            self.before[0][1].decrease(self.before[0][1].getN())
        self._setInformation(0, 0, 0)                         # 2022.12.21
        self._updateInfoAddUp()                               # 2022.12.21
        if EntropyCalc == "YES":
            self.forEntropyCalc.append((1, self.p))            # 2023.3.8
        else:
            self.forEntropyCalc.append((0, 0))                 # 2023.3.8
        

class allReaction:
    
    def __init__(self): 
        self.allReactions = {}
        
    def setReaction(self, ls, elems, normConst):
        className = ls[0].strip()
        rn = className + '_' + ls[1].strip()
        self._checkReactionName(rn)
        
        if   className == "r1_+" or className == "R1_+":
            after = self._makeList(ls[5:7], elems)
            self.allReactions[rn] = ReactionR0_1(rn, [], [ls[4], normConst] , after)

        elif   className == "r1_-" or className == "R1_-":
            before = self._makeList(ls[2:4], elems)
            self.allReactions[rn] = ReactionR0_0(rn, before, [ls[4], normConst] , [])

        elif   className == "r1_0" or className == "R1_0":
            before = self._makeList(ls[2:4], elems)
            self.allReactions[rn] = ReactionMulti(rn, before, [ls[4], normConst] , [])
            
        elif className == "r1_1" or className == "R1_1":
            self._defineReaction(elems, 2, 4, 5, 7, ls, rn, normConst)
            
        elif className == "r1_2" or className == "R1_2":
            self._defineReaction(elems, 2, 4, 5, 9, ls, rn, normConst)
            
        elif className == "r1_3" or className == "R1_3":
            self._defineReaction(elems, 2, 4, 5, 11, ls, rn, normConst)
            
        elif className == "r1_4" or className == "R1_4":
            self._defineReaction(elems, 2, 4, 5, 13, ls, rn, normConst)
            
        elif className == "r2_1" or className == "R2_1":
            self._defineReaction(elems, 2, 6, 7, 9, ls, rn, normConst)
            
        elif className == "r2_2" or className == "R2_2":
            self._defineReaction(elems, 2, 6, 7, 11, ls, rn, normConst)
            
        elif className == "r2_3" or className == "R2_3":
            self._defineReaction(elems, 2, 6, 7, 13, ls, rn, normConst)

        elif className == "r3_1" or className == "R3_1":
            self._defineReaction(elems, 2, 8, 9, 11, ls, rn, normConst)
            
        elif className == "r3_2" or className == "R3_2":
            self._defineReaction(elems, 2, 8, 9, 13, ls, rn, normConst)
            
        elif className == "r3_3" or className == "R3_3":
            self._defineReaction(elems, 2, 8, 9, 15, ls, rn, normConst)


    # The main code, binomial_xxx.py use this method.
    # The reactionManage_02.py also use this.    
    def setReactionMulti(self, ls1, ls2, ls3, elems):
        rn = ls1[0].strip() + '_' + ls1[1].strip()
        self._checkReactionName(rn)
        before = self._makeList(ls1[2:], elems)
        after = self._makeList(ls3, elems)
        self.allReactions[rn] = ReactionMulti(rn, before, ls2, after)
        print(rn, "in setReactionMulti")
        print(ls1, ls2, ls3)
        
    def _checkReactionName(self, rn):
        if rn in self.allReactions.keys():
            print("************** Error **************")
            print(f"Same reaction {rn} is defined!")
            print("Chack the reaction name in *Reaction.")
            sys.exit()
        

    def _defineReaction(self, elems, b1, b2, a1, a2, ls, rn, normConst):
        before = self._makeList(ls[b1:b2], elems)
        after = self._makeList(ls[a1:a2], elems)
        self.allReactions[rn] = ReactionMulti(rn, before, [ls[b2], normConst] , after)
        
        # error judgement
        all_len = len(before)*2 + len(after)*2 + 3
        if all_len == len(ls):
            pass
        else:
            print("*********** A error occured ***********")
            print()
            print(f"{ls[0]}_{ls[1]} definition was wrong.")
            print(f"The numbers of this needs {all_len} characters")
            print(" ")
            sys.exit()
        
    def _makeList(self, ls, elems):
        elemL = []
        itit = iter(ls)
        for order, element in zip(itit, itit):
            elemL.append([int(float(order)), elems[element]])  
        return elemL




