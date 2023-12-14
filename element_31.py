# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:19:35 2020

@author: takashi
"""

import random, sys
import numpy as np
import collections
import matplotlib

colorDict = matplotlib.colors.cnames
markers = ["o", "v", "^", "<", ">","1", "2", "3", "4", "8",  \
           "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
    
colors = ['Black', 'Green' ,'Yellow', 'Gray', 'Blue', 'Red', 'Orange']


class Element(object):    

    def __init__(self, name, initial, color, marker = ".", type = ""):  # 2022.10.2     
        self.name = name
        self.n = initial         
        self.color = color
        self.currentNums = [initial, ]
        self.marker = marker
        self.type = type         # is used in the polymer_xx.py
        # print("A element, ", name, initial, color, marker, type, " is created. ")

    
    def setNum(self, n):
        self.n = n
        self.currentNums.append(n) 
        
    def increase(self, dn):
        self.n += dn        

    def decrease(self, dn):
        self.n -= dn        
        
    def updateNumbers(self):
        self.currentNums.append(self.n) 
        
    def getN(self):
        return self.n


class ElementPolymer(Element):
    
    def __init__(self, name, initial, color, ls5, deg):
        self.degrees = deg
        
        print(f" self.degrees: {self.degrees}")
        super().__init__(name, initial, color, ".", ls5)  # 2022.9.10  name -> "."
    

class ElementInOut(Element):

    # 2022.10.2
    def __init__(self, name, initial, color, marker = ".", type = "", schedule_type = "type-0", *args):        
        super().__init__(name, initial, color, marker, type) 
        
        self.schedule_type = schedule_type
        self.args = args        
        self.schedule = []
        self.deltaN = []        
        print(" ElementInOut:  ", self.schedule_type, self.args)

    def calcSchedule(self, timeM):
        print("Calculate schedule for ElementInOut")        
        start = timeM.startTime
        end = timeM.endTime
        if self.schedule_type == "type-0":
            it = iter(self.args[0])
            for a, d in zip(it, it):  
                self.schedule.append(int(a))
                self.deltaN.append(int(d))
        elif self.schedule_type == "type-1":
            a = int(self.args[0][0])
            d = int(self.args[0][1])
            self.schedule = [ t for t in range(start, end + 1, a) ]
            self.deltaN = [ d for i in range(len(self.schedule)) ]
            self.deltaN[0] = self.n
        elif self.schedule_type == "type-2":
            s = int(self.args[0][0])
            a = int(self.args[0][1])
            T = int(self.args[0][2])
            d = int(self.args[0][3])
            self.schedule = [ t for t in range(start, end, d) ]
            self.deltaN = [ int(s + a*np.sin(2*np.pi*t*d/T)) for t in range(len(self.schedule)) ]            
            self.deltaN[0] = self.n
        print("Element in/out schedule and increments: ")
        print(self.schedule[:100], "\n", self.deltaN[:100])
    
    def getSchedule(self):
        pass


class allElements:

    def __init__(self):  
        self.allElements = {} 
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
        sa = Element(name, initial, color, marker, type)
        self.allElements[name] = sa


    def makeBasicEls(self, elN, usedBasicNames, maxTBNinEl):   # where use?    2022.12.24
        basicEls = []
        for i in range(elN):
            selected = random.choices(usedBasicNames, k = random.randint(1, maxTBNinEl))
            selectDic = dict(collections.Counter(selected))  
            basicEls.append(selectDic) 
        return basicEls 
      
    def makeName(self, basicEls):                           # where use?    2022.12.24
        elNames = []
        for el in basicEls:
            name = ""
            for k , v in el.items():
                name += k + "=" + str(v) + "_"
            name = name[:-1]
            elNames.append(name)
        return elNames

    def setNewLines(self, elNames, basicEls, initial3):   # where use?    2022.12.24
        for elName, elel in zip(elNames, basicEls):
            if elName in self.allElements.keys():
                # print(f"!! !! !!  Element  {elName} already exists !! !! !! ")
                pass
            else:
                colorName, colorCode = random.choice( list(colorDict.items()) )
                line = [elName, initial3, colorCode, " - ", "x", elel ]              # x means autoElement
                self.setElement(line)


    """
    define a element if There is NO in *Reaction.  Not used
    """
    # 2022.10.2
    # def setElementFromUtility(self, eName):
    #     if eName in self.allElements.keys():
    #         # print(f"!! !! !!  Element  {eName} already exists !! !! !! ")
    #         pass
    #     else:
    #         # print(f"!! !! !! New element  {eName} created !! !! !!")
    #         # initial = 0
    #         color = random.choice( list(colorDict.values()) )        
    #         # category = 'x'
    #         self.setElement([eName, 0, color, " - ", 'x', 0])


    def setElementInOut(self, ls):
        print(" ", )
        name, initial, color, marker = self._lineSprit(ls[:4])
        self._checkElementName(name)
        sa = ElementInOut(name, initial, color, marker, "InOut", ls[5], ls[6:])
        self.InOutElements[name] = sa
        self.allElements[name] = sa


    def setElementPolymer(self, ls):     
        nameChrList = list(ls[0])
        print(nameChrList)
        # This if-code should go to Polymer class.
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
            be = ElementPolymer(name, initial, color, ls[5], deg)
            self.allElements[newName] = be
            self.polymers[newName] = be


    def _checkElementName(self, name):
        if name in self.allElements.keys():
            print("************** Error **************")
            print(f"Same element {name} is defined!")
            print("Chack the element name in *Element or *ElementInOut.")
            sys.exit()

    def _lineSprit(self, ls):        
        name = ls[0].strip()
        initial = ls[1]
        color = ""
        try:
            initial = 0 if initial == "" else int(float(initial))
        except:
            initial = 0       
        try:
            color = random.choice(list(colorDict.values())) if ls[2] == "" else ls[2].replace(' ', '')
        except:
            color = random.choice(list(colorDict.values()))           
        try:                                                        # 2022.9.10
            marker = random.choice(markers) if ls[3] == "" else ls[3]
        except:
            marker = random.choice(markers)    
        return name, initial, color, marker


            
            