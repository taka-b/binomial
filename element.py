# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:19:35 2020

@author: Takashi Sato
"""


class Element:    

    def __init__(self, name, numbers, color):       
        self.name = name
        self.color = color
        self.n = numbers 
        self.currentNums = [ numbers, ]
#        self.localNameAndNum = { }      # 将来、番地と数を収める    
    
    def setNum(self, n):
        self.n = n
        self.currentNums.append(n) 
        
    def increase(self, dn):
        self.n += dn        

    def decrease(self, dn):
        self.n -= dn        
        
    def setReactionAll(self):
        self.currentNums.append(self.n) 
        
    def getN(self) :
        return self.n
  
        
        
class allElements:

    def __init__(self):  
        self.allElements = {} 
        
    def setElement(self, line_sprit):
        name = line_sprit[0].strip()
        initial = int(line_sprit[1])
        color = line_sprit[2].replace(' ', '')
        self.allElements[name] = Element(name, initial, color)


