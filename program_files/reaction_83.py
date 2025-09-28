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
from decimal import Decimal

import utility_functions as uf

UNIVERSE = 10**100

def set_Json_item(entropy = "", information = "", p_binomial = ""):
    global EntropyCalc, InformationCalc, p_Binomial
    EntropyCalc = entropy
    InformationCalc = information
    p_Binomial = p_binomial
    print(f'p_Binomial == "{p_Binomial}"')


class Reaction:
    
    def __init__(self, reactionName, before, reactionRate, normConst, after):
        self.reactionName = reactionName                            # Reaction name
        self.reactionName_history = [reactionName, ]
        self.prob = float(reactionRate)                             # probability
        self.normConst = uf.convert_to_int2(normConst)               # 2023.9.9: This is int.

        self.before = before                       # [[n1, el_b1],[n2, el_b2], --- ]
        self.after = after                         # [[m1, el_a1],[m2, el_a2], --- ]
        self.beforeElemNum = len(before)
        self.afterElemNum = len(after)
        self.p = self.prob/(1.0 + self.prob)       # 2022.8.23
        self.info = []                             # 2022.11.19 
        self.infoAddUp = []
        self.forEntropyCalc = []
        self.entropy = []
        self.n = []
        self.p_binomial = []
        print("Defined: " + reactionName + f"; {self.beforeElemNum} , {self.afterElemNum}")
        
    def rename(self, new_name):
        """Renames the reaction and records the change in the history."""
        self.reactionName_history.append(new_name)  # Save the current name to the history
        self.reactionName = new_name  # Update to the new name
           
    def react(self):   
        # 2024.4.21
        #elNumList = [el.getN()/order for order, el in self.before]
        try:
            elNumList = [int(Decimal(el.getN()) / Decimal(order)) for order, el in self.before]
        except OverflowError:
            print("OverflowError in react(): el.getN() too large")
            elNumList = [0] * len(self.before)        
        
        flg_info = 0
        
        if len(self.before) == 1:         # 2022.3.19
            p = self.p                    # 2022.8.23
            minNK = elNumList[0]          # 2022.5.21
        elif len(self.before) >= 2:
            minNK, p = self._getProb2(self.before)                  # 2022.3.15
            
        k = self._getIntK(minNK, p)
        
        if self._updateMulti(k, self.before, self.after) == 0:
            self._updateMulti(-k, self.before, self.after)          # 2022.11.19 
        elif k == 0:
            pass
        else:
            flg_info = 1
            
        if InformationCalc == "YES":
            self._set_infomation_Data(flg_info, k, minNK, p)
        elif InformationCalc == "NO" and EntropyCalc == "YES":
            self._set_infomation_Data(0, k, minNK, p)
        else:
            pass
        
        self._set_n_p(minNK, p)

    def _set_n_p(self, minNK, p):
        if p_Binomial == "YES" and minNK >= 0 and p >= 0:
            self.n.append(minNK)
            self.p_binomial.append(p)
        else:
            self.n.append("-")
            self.p_binomial.append("-")

    def _set_infomation_Data(self, flg_info, k, minNK, p):
        if flg_info == 0:
            self._setInformation(0, 0, 0) 
        else:
            self._setInformation(k, minNK, p)
        self._updateInfoAddUp()                                     # 2022.11.19
        
        if EntropyCalc == "YES":
            self.forEntropyCalc.append((minNK, p))                  # 2023.3.2
        else:
            self.forEntropyCalc.append((0, 0))                      # 2023.3.2

    def _set_entropy_data(self, minNK, p):
        self.forEntropyCalc.append((minNK, p))
    
    # 2024.4.20
    def _getProb2(self, before):
        try:
            minNK = UNIVERSE
            min_el = None
            min_el_num = 0
            max_order_for_mini_el = 1
            max_order_flg = 0
            non_min = []
            p = 1
            
            # Find the element with the smallest unit count
            for order, el in before:
                nk = int(Decimal(el.getN()) / Decimal(order))
                if nk < minNK:
                    minNK = nk
                    min_el = el
            
            # Count how many times the smallest unit element appears in before
            for order, el in before:
                if el == min_el:
                    min_el_num += 1
            
            # Prevent division by zero when adjusting minNK based on the count of min_el
            if minNK > 0 and min_el_num > 0:
                minNK = int(minNK/min_el_num)
            else:
                minNK = 0
            
            # Find the maximum order value among elements that match min_el
            for order, el in before:                
                if order > max_order_for_mini_el and el == min_el:
                    max_order_for_mini_el = order
            
            # Exclude the first occurrence of min_el with the maximum order, add others to non_min
            for order, el in before:
                if order == max_order_for_mini_el and el == min_el and max_order_flg == 0:
                    max_order_flg = 1
                else:
                    non_min.append([order, el])
            
            for order, el in non_min:
                prob = Decimal(self.prob)*(Decimal(el.getN())/Decimal(order))/Decimal(self.normConst)
                prob = min(prob, Decimal(1e308))
                p *= prob/(Decimal('1.0') + prob)
    
            return minNK, p
    
        except Exception as e:
            # Any exception (like zero division) results in zero return values
            print(e)
            return 0, 0

    # 2024.4.20
    def _getIntK(self, n, p):
        try:
            # random.gauss is used for large int
            n = Decimal(n)  # to Decimal 
            p = Decimal(p)
            if n > Decimal(1e15):
                mean = n * p
                stddev = (n * p * (1 - p)).sqrt()
                k = random.gauss(float(mean), float(stddev))
            else:
                k = np.random.binomial(int(n), float(p))
            return int(k)
        except Exception:
            print("Error: in _getIntK(self, n, p)")
            return 0


    def _updateMulti(self, k, before, after):
        flg = 1
        for order, el in before:
            k_decimal = Decimal(k)
            order_decimal = Decimal(order)
            el.decrease(int(k_decimal*order_decimal))
            flg *= 0 if (el.getN() < 0 and k > 0) else 1
        for order, el in after:
            el.increase(order*k)   
        return flg
    
    # 2022.11.19
    def _setInformation(self, k, N, p):
        try:                                #  2025.2.19
            bi_pmf = binom.pmf(k, N, p)
            if bi_pmf > 0:
                self.info.append(-math.log2(bi_pmf))
            else:
                self.info.append(0)
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
        super()._set_n_p(1, self.p)
        

# 2022.8.23  2023.9.19
class ReactionR1_minus(Reaction):
    
    def __init__(self, reactionName, before, reactionRate, normConst, after):
        super().__init__(reactionName, before, reactionRate, normConst, after)
        
    def react(self):    
        k = super()._getIntK(1, self.p)                       # 2022.12.21  
        if super()._updateMulti(k, self.before, self.after) == 0:    
            self.before[0][1].decrease(self.before[0][1].getN())              # 2024.3.30, self <-- super() 
        
        super()._set_infomation_Data(0, k, 1, self.p)        
        super()._set_n_p(1, self.p)

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
        
        super()._set_infomation_Data( 0, 0, 1, 1)               # 2024.2.2 
        super()._set_n_p(0, 1)                                   # 2024.4.18 
            
# class reactions:                                    # 2025.1.8
class AllReactions:                                     # 2025.1.8
    
    def __init__(self): 
        self.reactions = {}
        
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
            
        elif className == "r2_0" or className == "R2_0":
            self._defineReaction(elements, 2, 6, -1, -1, ls, reactionName, normConst)
            
        elif className == "r2_1" or className == "R2_1":
            self._defineReaction(elements, 2, 6, 7, 9, ls, reactionName, normConst)
            
        elif className == "r2_2" or className == "R2_2":
            self._defineReaction(elements, 2, 6, 7, 11, ls, reactionName, normConst)
            
        elif className == "r2_3" or className == "R2_3":
            self._defineReaction(elements, 2, 6, 7, 13, ls, reactionName, normConst)

        elif className == "r3_0" or className == "R3_0":
            self._defineReaction(elements, 2, 8, -1, -1, ls, reactionName, normConst)

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
            elems.append([uf.convert_to_int2(coeff), elements[element]])  
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
        if float(reactionRate) < 0:
            print("At *Reaction definition stage: ")
            sys.exit("Error: Reaction rate is under ZERO. It munst be larger than ZERO.")   

    def _defineReaction(self, elements, b1, b2, a1, a2, ls, reactionName, normConst):
        before = self._makeList(ls[b1:b2], elements)
        if a1 == -1 and a2 == -1:
            after = []
            all_len = len(before)*2 + 3
            if all_len == len(ls):                             # 2023.5.7
                pass
            else:
                print()
                print(f"{ls[0]}_{ls[1]} definition was wrong.")
                sys.exit(f"The number of reaction-terms needs {b2} characters")
        else:
            after = self._makeList(ls[a1:a2], elements)       
            all_len = len(before)*2 + len(after)*2 + 3
            if all_len == len(ls) and len(ls) == a2:                             # 2023.5.7
                pass
            else:
                print()
                print(f"{ls[0]}_{ls[1]} definition was wrong.")
                sys.exit(f"The number of reaction-terms needs {a2} characters")
        
        self._check_normConst(normConst)    
        self._check_reactionRate(float(ls[b2]))
        self.reactions[reactionName] = Reaction(reactionName, before, ls[b2], normConst, after)            
        
    def _makeList(self, ls_x, elements):
        elems = []
        itit = iter(ls_x)
        for order, element in zip(itit, itit):
            elems.append([uf.convert_to_int2(order), elements[element]])  
        return elems

    
    def createReactionPolymer(self, ls, all_elements, normConst):
        if ls[0] == "rP_elong":
            for el, el_obj in all_elements.elements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees + int(ls[4])
                    after = self._getAfterPolymer("M=*_R", deg, all_elements)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(el_obj.degrees), ls[2], el, ls[4], ls[5]]
                        ls3 = [ls[7], after]
                        self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements) 
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
                             ls3 = [ls[7], after]
                             self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.polymers) 
        elif ls[0] == "rP_trans":
            print("\n in rP_trans")
            for el_1, el_obj_1 in all_elements.polymers.items():
                deg_1 = el_obj_1.degrees
                for el_2, el_obj_2 in all_elements.polymers.items():
                    deg_2 = el_obj_2.degrees
                    if el_obj_1.type == "M=*_R" and el_obj_2.type == "M=*" and deg_1 <= deg_2:
                        after_1 = self._getAfterPolymer("M=*", deg_1, all_elements)
                        after_2 = self._getAfterPolymer("M=*_R", deg_2, all_elements)
                        if after_1 != "" and after_2 != "":
                            ls1 = ["r2_2", ls[1]+"_"+str(deg_1) + "+" + str(deg_2), ls[2], el_1, ls[4],  el_2]
                            ls3 = [ls[7], after_1, ls[9], after_2]
                            self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements)
        elif ls[0] == "rP_dispro":
            print("in rP_dispro")
            for el_1, el_obj_1 in all_elements.polymers.items():
                deg_1 = el_obj_1.degrees
                for el_2, el_obj_2 in all_elements.polymers.items():
                    deg_2 = el_obj_2.degrees
                    if el_obj_1.type == "M=*_R" and el_obj_2.type == "M=*_R" and deg_1 <= deg_2:
                        after_1 = self._getAfterPolymer("M=*", deg_1, all_elements)
                        after_2 = self._getAfterPolymer("M=*", deg_2, all_elements)
                        ls1 = ["r2_2", ls[1]+"_"+str(deg_1) + "+" + str(deg_2), ls[2], el_1, ls[4], el_2]
                        ls3 = [ls[7], after_1, ls[9], after_2]
                        self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements)
        elif ls[0] == "rP_react_01":
            print("in rP_react_01")
            for el, el_obj in all_elements.elements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees
                    after = self._getAfterPolymer("M=*", deg, all_elements)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(deg), ls[2], el, ls[4], ls[5]]
                        ls3 = [ls[7], after]
                        self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements) 
        elif ls[0] == "rP_react_02":
            print("in rP_react_02")
            for el, el_obj in all_elements.elements.items():
                if el_obj.type == "M=*":
                    deg = el_obj.degrees
                    after = self._getAfterPolymer("M=*_R", deg, all_elements)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(deg), ls[2], el, ls[4], ls[5]]
                        ls3 = [ls[7], after]
                        self.setReactionMulti(ls1, ls[6], normConst, ls3, all_elements.elements) 
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
