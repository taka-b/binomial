# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:19:35 2020

@author: takashi
"""

import random, sys
import numpy as np
import matplotlib
# import re, sys

import utility_functions as uf

colorDict = matplotlib.colors.cnames
markers = ["o", "v", "^", "<", ">","1", "2", "3", "4", "8",  \
           "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
    
colors = ['Black', 'Green' ,'Yellow', 'Gray', 'Blue', 'Red', 'Orange']


class Element(object):    

    def __init__(self, name, initial, color, marker = ".", type = ""):  # 2022.10.2     
        self.name = name
        self.name_history = [name, ]
        self.n = initial
        self.n_previous = 0
        self.color = color
        self.currentNums = [initial, ]
        self.marker = marker
        self.type = type         # is used in the polymer_xx.py
        self.plotNumbers = [initial, ]
        self.csvNumbers = [initial, ]
        print(self.name, ": ",self.n)              # 2024.3.28
        
    def increase(self, dn):
        self.n += dn      
        if self.n > 1e300:
            self.n = 1e299

    def decrease(self, dn):
        self.n -= dn        
        
    def updateNumbers(self):
        self.currentNums.append(self.n)
        
    def getN(self):
        return self.n
    
    def rename(self, new_name):
        """Renames the element and records the change in the history."""
        self.name_history.append(new_name)  # Save the current name to the history
        self.name = new_name  # Update to the new name
   
    def append_csvNumbers(self):
        pass
    
    def append_plotNumbers(self):
        self.plotNumbers.append(self.n)
    

class ElementSet(Element):
    
    def __init__(self, name, initial, color, 
                 elements, 
                 reactions,
                 plots,
                 marker = ".", type = ""):  # 2023.1.30
        
        super().__init__(name, initial, color, marker, "Set")
        
        self.elements = []
        self.reactions = []
        self.plots = []


class ElementPolymer(Element):
    
    def __init__(self, name, initial, color, ls5, deg):
        self.degrees = deg
        
        # print(f" self.degrees: {self.degrees}")
        super().__init__(name, initial, color, ".", ls5)  # 2022.9.10  name -> "."
    

class ElementInOut(Element):

    # 2022.10.2
    def __init__(self, name, initial, color, marker = ".", type = "", 
                 schedule_type = "type-0",
                 *args):        
        super().__init__(name, initial, color, marker, type) 
        
        self.schedule_type = schedule_type
        self.args = args        
        self.schedule = []
        self.deltaN = []        

    def calcSchedule(self, timeM):
        print("Calculate a schedule for the ElementInOut!")        
        start = timeM.startTime
        end = timeM.endTime
        if self.schedule_type == "type-0":
            it = iter(self.args[0])
            for a, d in zip(it, it):
                # InOut time should be uf.convert_to_int2(a)-1, because of time schedule.
                # Please look at def calculate() in the main program of binomial_xxx.py  
                self.schedule.append(uf.convert_to_int2(a)-1)             # 2024.3.28
                self.deltaN.append(uf.convert_to_int2(d))
        elif self.schedule_type == "type-1":
            a = uf.convert_to_int2(self.args[0][0])
            d = uf.convert_to_int2(self.args[0][1])
            print(a, d, "in def calcSchedule")
            self.schedule = [ t for t in range(start, end + 1, a) ]    # 2023.11.26
            self.deltaN = [ d for i in range(len(self.schedule)) ]
        elif self.schedule_type == "type-2":
            s = uf.convert_to_int2(self.args[0][0])
            a = uf.convert_to_int2(self.args[0][1])
            T = uf.convert_to_int2(self.args[0][2])
            d = uf.convert_to_int2(self.args[0][3])
            self.schedule = [ t for t in range(start, end, d) ]
            self.deltaN = [int(s + a*np.sin(2*np.pi*t*d/T)) for t in range(len(self.schedule))]            
            self.deltaN[0] = self.n
        else:
            print('The *ElementInOut needs "type-0", "type-1", and "type-2" ')
            sys.exit()
        # print("self.schedule: ", self.schedule)
        # print("self.deltaN: ", self.deltaN)

class AllElements:

    def __init__(self):  
        self.elements = {} 
        self.polymers = {}
        self.distributionOfPolymer = {}
        self.InOutElements = {}
    
    def setElement(self, ls):                                # needs refactering        
        name, initial, color, marker = self._lineSprit(ls)    # 2022.9.10
        self._checkElementName(name)
        try:
            type = ls[4]
            type = "?" if type == "" else ls[4].replace(' ', '')         
        except:
            type = "?"    
        el = Element(name, initial, color, marker, type)
        self.elements[name] = el

    def setElementInOut(self, ls):
        print(" ", )
        name, initial, color, marker = self._lineSprit(ls[:4])
        self._checkElementName(name)
        initial = uf.convert_to_int2(initial)
        ei = ElementInOut(name, initial, color, marker, "InOut", ls[5], ls[6:])
        print("ls[6:]: ", ls[6:])
        self.InOutElements[name] = ei
        self.elements[name] = ei 

    def setElementPolymer(self, ls):     
        nameChrList = list(ls[0])
        print("nameChrList: ", nameChrList)
        if "M" not in nameChrList:
            print()
            print("***  Error  ***")
            print("Use \"M\" for monomer in Polymerization process!!")                       
            sys.exit()
        for deg in range(int(ls[1]), int(ls[2]) + int(ls[3]) , int(ls[3])):
            nameChrList = list(ls[0])
            indx = [i for i, x in enumerate(nameChrList) if x == '*']
            nameChrList[indx[0]] = str(deg) 
            newName = ''.join(nameChrList)
            name, initial, color, marker = self._lineSprit([newName, ls[4], ""])
            self._checkElementName(name)
            ep = ElementPolymer(name, initial, color, ls[5], deg)
            self.elements[newName] = ep
            self.polymers[newName] = ep


    def _checkElementName(self, name):
        if name in self.elements.keys():
            print()
            print("**********_checkElementName Error **********")
            print(f"Same element {name} is defined!")
            print("Chack the element name in *Element or *ElementInOut.")
            sys.exit()

    def _lineSprit(self, ls):        
        name = ls[0].strip()
        initial = uf.convert_to_int2(ls[1])
        
        color = ""
        try:
            color = random.choice(list(colorDict.values())) if ls[2] == "" else ls[2].replace(' ', '')
        except:
            color = random.choice(list(colorDict.values()))           
        
        try:                                                        # 2022.9.10
            marker = random.choice(markers) if ls[3] == "" else ls[3]
        except:
            marker = random.choice(markers)    
        return name, initial, color, marker


            
            