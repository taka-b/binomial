# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:19:35 2020

@author: takashi
"""


class Element:    

    def __init__(self, name, numbers, color, realName):       
        self.name = name
        self.color = color
        self.n = numbers 
        self.currentNums = [ numbers, ]
        self.realName = realName
        #self.localNameAndNum = { }      # 将来、番地と数を収める    
    
    def setNum(self, n):
        self.n = n
        self.currentNums.append(n) 
        
    def increase(self, dn):
        self.n += dn        

    def decrease(self, dn):
        self.n -= dn        
        
    def updateNumbers(self):
        self.currentNums.append(self.n) 
        
    def getN(self) :
        return self.n
  
    

# class Cell(Element):
    elementCount = 0
    
#     pass
        

class Genome(Element):
    
    def __init__(self, name, numbers, color, elem) :    
        super().__init__(name, numbers, color)
        self.nucleicAcidSet = [ elem, ]    

        
class DNA(Element):

    def __init__(self, name, numbers, color, elem) :    
        super().__init__(name, numbers, color)
        self.nucleicAcidSet = [ elem, ]
                
    def calcTotal(  ):
        pass
    
    def polymerize(self, elem):
        self.nucleicAcidSet.append(elem)
        pass
    

class RNA(Element):

    def __init__(self, name, numbers, color, elem) :    
        super().__init__(name, numbers, color)
        self.nucleicAcidSet = [ elem, ]
                
    def calcTotal(  ):
        pass
    
    def polymerize(self, elem):
        self.nucleicAcidSet.append(elem)
        pass


class Protain(Element):

    def __init__(self, name, numbers, color) :    
        super().__init__(name, numbers, color)
        self.aminoAcidSet = [ ]
                
    def calcTotal(  ):
        pass
    
    def polymerize(self, elem):
        self.aminoAcidSet.append(elem)
        pass

    

# class Complex(Element):
    
#     def __init__(self, name, emts, color) :
#         self.emts = emts   
#         self.cN = self.calcNum( )       
#         super( ).__init__( name, self.cN, color )
                
#     def calcNum( self ):
#         rn = 0
#         for i in range(len(self.emts)) :
#             rn = rn + self.emts[i].n
#         return rn

        
        
class allElements:

    def __init__(self):  
        self.allElements = {} 
        
    def setElement(self, line_sprit):
        name = line_sprit[0].strip()
        initial = int(line_sprit[1])
        color = line_sprit[2].replace(' ', '')
        realName = line_sprit[3].replace(' ', '')
        self.allElements[name] = Element(name, initial, color, realName)


