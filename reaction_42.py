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


PROB_PARA = 0.9   # 2021.11.7  --> 4.18
PROB_PARA_2 = 0.1   # 2021.11.7
UNIVERSE = 10**100
    
class ReactionMulti:
    
    def __init__(self, rn, before, ls2, after):
        self.rName = rn                            # Reaction name
        self.prob = float(ls2[0])                  # probability
        self.all = int(float(ls2[1]))              # Reaction area        
        self.beforeElemNum = len(before)
        self.before = before                       # [[n1, el_b1],[n2, el_b2], --- ]
        self.after = after                         # [[m1, el_a1],[m2, el_a2], --- ]
        # self.before_increment = 0             # 2022.3.21  not used!
        # self.after_increment = 0              # 2022.3.21  not used!
        self.p = self.prob/(1.0 + self.prob)  # 2022.8.23
        self.info = [0, ]                                             # 2022.11.19 
        self.infoAddUp = [0, ]
           
    def react(self):                          # 2022.3.20
        # 2022.5.11
        elNumList = [el.getN()/order for order, el in self.before]
        if 0 in elNumList:
            self._setInformation(0, 0, 0)                              # 2022.11.19 
            self._updateInfoAddUp()  
        else:
            # self.before_increment = 0         # 2022.3.21
            # self.after_increment = 0          # 2022.3.21
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
            self._updateInfoAddUp()                                   # 2022.11.19
            
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
            # self.before_increment = -order*k 
            flg *= 0 if (el.getN() < 0 and k > 0) else 1
        for order, el in after:
            el.increase(order*k)   
            # self.after_increment = order*k 
        return flg
    
    # 2022.11.19
    def _setInformation(self, k, N, p):
        if p == 0 :
            self.info.append(0)
        else:
            try:
                if binom.pmf(k, N, p) == 0.0 :     # 2022.12.23  
                    self.info.append(0)            # 2022.12.1
                else:
                    self.info.append(-math.log2(binom.pmf(k, N, p)))    # 2022.12.1  
            except:
                self.info.append(0)
            
    def _updateInfoAddUp(self):
        nextValue = self.infoAddUp[-1] + self.info[-1]
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

# 2022.3.20
# reaction definition for r2_1-1
class ReactionCell(ReactionMulti):
    
    def __init__(self, rn, before, ls2, after, decrease):
        super().__init__(rn, before, ls2, after)
        self.cellIncrement = 0
        self.decrease = decrease
        self.decreaseElement = decrease[0][1]   
        print("Reaction element: ", self.decreaseElement.name)
        
    def react(self):
        # except for Cell
        super().react()  
        # for Cell
        # still with a bug !!!
        self.cellIncrement = self.after_increment
        # self.cellIncrement = self.after[0][1].n - self.after[0][1].currentNums[-1]
        print("cell increment: ", self.cellIncrement)
        flg = self._updateMulti(self.cellIncrement, self.decrease, []) 
        print("flg: ", flg)
        if flg == 0:
            self.whileProcess(self.cellIncrement,
                                   self.rName,
                                   self.before[0], self.before, self.after, self.prob,
                                   self.decreaseElement)

    def whileProcess(self, k, rName, minmum_element, before, after, prob, decreaseElement):
        flg = 0
        while(flg == 0):
            print(f"while roop in class ReactionMulti in {self.rName} !!")            
            # resrt the numbers
            flg = self._updateMulti(-k, before, after)
            decreaseElement.increase(k) 
            # new prob
            prob = prob * PROB_PARA_2                    # 2022.3.21
            print(f"self.prob change to {prob} from {self.prob}")
            k = self._getIntK(minmum_element[1].getN(), prob)
            self._updateMulti(k, before, after)
            self.cellIncrement = self.after_increment
            # self.cellIncrement = self.after[0][1].n - self.after[0][1].currentNums[-1]
            print("cell increment: ", self.cellIncrement)
            # judge 
            flg = self._updateMulti(self.cellIncrement, self.decrease, []) 


# 2022.3.21
# reaction definition for r1_1-2
class ReactionCell_02(ReactionMulti):
    
    def __init__(self, rn, before, ls2, after, decrease):
        super().__init__(rn, before, ls2, after)
        self.Increment_01 = 0
        self.Increment_02 = 0
        self.decrease = decrease
        self.decreaseElement_01 = decrease[0][1]
        self.decreaseElement_02 = decrease[1][1]   
        print("Decrease element 1: ", self.decreaseElement_01.name)
        print("Decrease element 2: ", self.decreaseElement_02.name)
        
    def react(self):
        #  except for Cell
        super().react()  
        # for cell or receptorOnCell
        # still with a bug !!!
        increment = self.after_increment
        # increment = self.after[0][1].n - self.after[0][1].currentNums[-1]
        print("increment: ", increment)
        self.Increment_01 = self.decrease[0][0]*increment
        self.Increment_02 = self.decrease[1][0]*increment
        print("cell increment_01: ", self.Increment_01)
        print("cell increment_02: ", self.Increment_02)
        flg = self._updateMulti(increment, self.decrease, []) 
        print("flg: ", flg)
        if flg == 0:
            self.whileProcess(increment, self.rName,
                              self.before[0], self.before, self.after, self.prob)

    def whileProcess(self, increment, rName, minmum_element, before, after, prob):
        flg = 0
        while(flg == 0):
            print(f"while roop in class ReactionMulti in {self.rName} !!")            
            # resrt the numbers
            flg = self._updateMulti(-increment, before, after)
            self.decreaseElement_01.increase(increment*self.decrease[0][0])
            self.decreaseElement_02.increase(increment*self.decrease[1][0]) 
            # new prob
            prob = prob * PROB_PARA_2                    # 2022.3.21
            print(f"self.prob change to {prob} from {self.prob}")
            k = self._getIntK(minmum_element[1].getN(), prob)
            self._updateMulti(k, before, after)
            increment = self.after_increment
            # increment = self.after[0][1].n - self.after[0][1].currentNums[-1]
            self.Increment_01 = self.decrease[0][0]*increment
            self.Increment_02 = self.decrease[1][0]*increment
            print("cell increment_01: ", self.Increment_01)
            print("cell increment_02: ", self.Increment_02)
            # judge
            flg = self._updateMulti(increment, self.decrease, []) 
        

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

        # 2022.10.2
        # elif className == "r2_1-1" or className == "R2_1-1":
        #     before = self._makeList(ls[3:5], elems)
        #     after = self._makeList(ls[6:8], elems)
        #     decrease = self._makeList(["1", ls[2]], elems)
        #     self.allReactions[rn] = ReactionCell(rn, before, [ls[5], normConst], after, decrease) 

        # elif className == "r1_1-2" or className == "R1_1-2":
        #     before = self._makeList(ls[2:4], elems)
        #     after = self._makeList(ls[5:7], elems)
        #     decrease = self._makeList(ls[7:11], elems)
        #     self.allReactions[rn] = ReactionCell_02(rn, before, [ls[4], normConst], after, decrease)   

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
            elemL.append([int(order), elems[element]])
        return elemL




















        
            
        
        
        
        
        