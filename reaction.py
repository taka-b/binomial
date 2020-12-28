# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:53:34 2020

@author: takashi
"""

import numpy as np


PROB_PARA = 0.5
DUMMY_NUM = 1

class Reaction:

    def __init__(self, name, all, n1, a, n2, b, n3, c, p, n4, x, n5, y, n6, z):
        self.name = name
        self.all = all
        self.n1 = n1          
        self.a = a
        self.n2 = n2          
        self.b = b  
        self.n3 = n3          
        self.c = c  
        self.p = p
        self.n4 = n4
        self.x = x       
        self.n5 = n5
        self.y = y     
        self.n6 = n6
        self.z = z   

    def getK1(self, a, p):
        if p < 0 or p > 1  :
            print(" p must be 0 < p < 1.", "p = ", p)
        while( p > 1 ):
            p = p * PROB_PARA
        return int(np.random.binomial(a.getN(), p, 1))


    def getK1_02(self, a, p):
        prob = a.getN()*p/self.all        
        if p < 0 or p > 1  :
            print(" p must be 0 < p < 1. ", " prob = ", prob)
        while( p > 1 ):
            p = p * PROB_PARA/self.all
        return int(np.random.binomial(a.getN(), p, 1))


    def getK2(self, a, b, p):
        if (a.getN() > b.getN()):
            prob = a.getN()*p/self.all
            while(prob > 1):
                # print("while roop in getK2 : ", "prob = ", prob)                 
                p = p * PROB_PARA
                prob = a.getN()*p/self.all  
            k = np.random.binomial(b.getN(), prob, 1)
        else:
            prob = b.getN()*p/self.all
            while(prob > 1):
                # print("while roop in getK2 : ", "prob = ", prob)  
                p = p * PROB_PARA
                prob = b.getN()*p/self.all               
            k = np.random.binomial(a.getN(), prob, 1)
        return int(k)

    
    def getK2_02(self, a, b, p):
        prob = a.getN()*b.getN()*p/self.all**2
        if prob > 1 :
            print("**************** In getK2 ******************* : ", "prob = ", prob)   
        while(prob > 1):
            p = p * PROB_PARA                   
            prob = a.getN()*b.getN()*p/self.all**2 
        if  a.getN() < b.getN() :
            k = np.random.binomial(a.getN(), prob, 1)         
        else:
            k = np.random.binomial(b.getN(), prob, 1)
        return int(k)


    def getK3(self, a, b, c, p):
        pass


    def getK3_02(self, a, b, c, p):
        prob = a.getN()*b.getN()*c.getN()*p/self.all**3
        if prob > 1 :
            print("**************** In getK3_02 ******************* : ", "prob = ", prob)   
        while(prob > 1):
            # print("while roop in getK3_02 : ", "prob = ", prob)   
            p = p * PROB_PARA            
            prob = a.getN()*b.getN()*c.getN()*p/self.all**3
        if   a.getN() < b.getN() and a.getN() < c.getN():
            k = np.random.binomial(a.getN(), prob, 1)
        elif b.getN() < a.getN() and b.getN() < c.getN():
            k = np.random.binomial(b.getN(), prob, 1)     
        else:
            k = np.random.binomial(c.getN(), prob, 1)  
        return int(k)             

            
    def checkNumAll(self, cList):
        for elem in cList:
            if elem.getN() < 0:
                flg = 0
                break
            else:
                flg = 1          
        return flg
    
    
    def update(self, k):
        self.a.decrease(self.n1*k)
        self.b.decrease(self.n2*k) if self.n2 > 0 else 1              # 1 is dummy. This means pass.
        self.c.decrease(self.n3*k) if self.n3 > 0 else 1 
        self.x.increase(self.n4*k) if self.n4 > 0 else 1
        self.y.increase(self.n5*k) if self.n5 > 0 else 1    
        self.z.increase(self.n6*k) if self.n6 > 0 else 1            
        
        if   self.n2 > 0 and self.n3 > 0:
            flg = 1 if k < 0 else self.checkNumAll([self.a, self.b, self.c]) 
        elif self.n2 > 0 and self.n3 == 0:
            flg = 1 if k < 0 else self.checkNumAll([self.a, self.b]) 
        else:
            flg = 1 if k < 0 else self.checkNumAll([self.a])
        return flg 


    def whileProcess(self, className, k, p):
        flg = 0
        while(flg == 0):
            print(f"while roop in class {className} : ", f"NEGATIVE ELEMENT in {self.name} !!" )
            flg = self.update(-k)
            p = p * PROB_PARA
            if   self.n2 == 0 and  self.n3 == 0 :
                k = self.getK1(self.a, p)
            elif self.n3 == 0:
                k = self.getK2(self.a, self.b, p)
            else:
                k = self.getK3_02(self.a, self.b, self.c, p)
            flg = self.update(k)



class r_1_0(Reaction):
    
    def __init__(self, name, n1, a, p):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, 0, None, p, 0, None, 0, None, 0, None)        
        
    def react(self): 
        k = self.getK1(self.a, self.p) 
        if self.update( k ) == 0:
            self.whileProcess("r_1_0", k, self.p)         


class r_1_1(Reaction):
    
    def __init__(self, name, n1, a, p, n4, x):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, 0, None, p, n4, x, 0, None, 0, None)           
        
    def react(self): 
        k = self.getK1(self.a, self.p) 
        if self.update( k ) == 0:
            self.whileProcess("r_1_1", k, self.p)

        
class r_1_2(Reaction):
    
    def __init__(self, name, n1, a, p, n4, x, n5, y):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, 0, None, p, n4, x, n5, y, 0, None)       
        
    def react(self): 
        k = self.getK1(self.a, self.p)
        if self.update( k ) == 0:
            self.whileProcess("r_1_2", k, self.p)


class r_1_3(Reaction):
    
    def __init__(self, name, n1, a, p, n4, x, n5, y, n6, z):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, 0, None, p, n4, x, n5, y, n6, z)       
        
    def react(self): 
        k = self.getK1(self.a, self.p)
        if self.update( k ) == 0:
            self.whileProcess("r_1_3", k, self.p)


class r_2_1(Reaction):
    
    def __init__(self, name, all, n1, a, n2, b, p, n4, x):
        super().__init__(name, all, n1, a, n2, b, 0, None, p, n4, x, 0, None, 0, None)
        
    def react(self):       
        k = self.getK2(self.a, self.b, self.p)   # 2020.12.5
        if self.update( k ) == 0:
            self.whileProcess("r_2_1", k, self.p)


class r_2_2(Reaction):
    
    def __init__(self, name, all, n1, a, n2, b, p, n4, x, n5, y):
        super().__init__(name, all, n1, a, n2, b, 0, None, p, n4, x, n5, y, 0, None)     
        
    def react(self):       
        k = self.getK2(self.a, self.b, self.p)   # 2020.12.5
        if self.update( k ) == 0:
            self.whileProcess("r_2_2", k, self.p)
            

class r_3_1(Reaction):
    
    def __init__(self, name, all, n1, a, n2, b, n3, c, p, n4, x):
        super().__init__(name, all, n1, a, n2, b, n3, c, p, n4, x, 0, None, 0, None)
        
    def react(self):        
        k = self.getK3_02(self.a, self.b, self.c, self.p)
        if self.update( k ) == 0:
            self.whileProcess("r_3_1", k, self.p)


class allReaction:
    
    def __init__(self): 
        self.allReactions = {}
        self.all = 0

    def setReaction(self, ls, elem):
        className = ls[0].strip()
        rn = ls[0].strip() + '_' + ls[1].strip()
        
        if   className == "r1_0" or className == "R1_0":
            self.allReactions[rn] = r_1_0(rn, int(ls[2]), elem[ls[3]], float(ls[4]))
            
        elif className == "r1_1" or className == "R1_1":
            self.allReactions[rn] = r_1_1( rn, int(ls[2]), elem[ls[3]], float(ls[4]), \
                                          int(ls[5]), elem[ls[6]])

        elif className == "r1_2" or className == "R1_2":
            self.allReactions[rn] = r_1_2(rn, int(ls[2]), elem[ls[3]], float(ls[4]), \
                                          int(ls[5]), elem[ls[6]], \
                                              int(ls[7]), elem[ls[8]])

        elif className == "r1_3" or className == "R1_3":
            self.allReactions[rn] = r_1_3(rn, int(ls[2]), elem[ls[3]], float(ls[4]), \
                                          int(ls[5]), elem[ls[6]], \
                                              int(ls[7]), elem[ls[8]], int(ls[9]), elem[ls[10]])
        
        elif className == "r2_1" or className == "R2_1":
            self.allReactions[rn] = r_2_1(rn, self.all, int(ls[2]), elem[ls[3]], \
                                          int(ls[4]), elem[ls[5]], float(ls[6]), \
                                              int(ls[7]), elem[ls[8]])
        
        elif className == "r2_2" or className == "R2_2":
            self.allReactions[rn] = r_2_2(rn, self.all, int(ls[2]), elem[ls[3]], \
                                          int(ls[4]), elem[ls[5]], float(ls[6]), \
                                              int(ls[7]), elem[ls[8]], \
                                                  int(ls[9]), elem[ls[10]])
                
        elif className == "r3_1" or className == "R3_1":
            self.allReactions[rn] = r_3_1(rn, self.all, int(ls[2]), elem[ls[3]], \
                                          int(ls[4]), elem[ls[5]], int(ls[6]), elem[ls[7]], float(ls[8]), \
                                              int(ls[9]), elem[ls[10]])
        else:
            pass





















        
            
        
        
        
        
        