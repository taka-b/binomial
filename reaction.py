# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:53:34 2020

@author: Takashi Sato
"""

import numpy as np


PROB_PARA = 0.9
DUMMY_NUM = 1

class Reaction:

    def __init__(self, name, all, n1, a, n2, b, p, n3, x, n4, y):
        self.name = name
        self.all = all
        self.n1 = n1          
        self.a = a
        self.n2 = n2          
        self.b = b  
        self.p = p
        self.n3 = n3
        self.x = x       
        self.n4 = n4
        self.y = y     

    def getK1(self, a, p):
        return int(np.random.binomial(a.getN(), p, 1))

    def getK2(self, a, b, p):
        if (a.getN() > b.getN()):
            prob = a.getN()*p/self.all
            while( prob > 1 ):
                print("while roop in getK2 : ", "prob = ", prob)                 
                p = p * PROB_PARA
                prob = a.getN()*p/self.all  
            k = np.random.binomial(b.getN(), prob, 1)
        else:
            prob = b.getN()*p/self.all
            while( prob > 1 ):
                print("while roop in getK2 : ", "prob = ", prob)  
                p = p * PROB_PARA
                prob = b.getN()*p/self.all               
            k = np.random.binomial(a.getN(), prob, 1)
        return int(k)

    def checkNumAll(self, cList):
        for elem in cList:
            if elem.getN() < 0:
                flg = 0
                break
            else:
                flg = 1          
        return flg
    
    # The k<0 means recovery process. Then flg always is 1.  
    def update1_0(self, n1, a, k):
        a.decrease(n1*k)
        flg = 1 if k < 0 else self.checkNumAll([a]) 
        return flg   

    def update(self, n1, a, n2, b, k, n3, x, n4, y):
        a.decrease(n1*k)
        b.decrease(n2*k) if n2 > 0 else 1   # 1 is dummy. It means pass.
        x.increase(n3*k) if n3 > 0 else 1
        y.increase(n4*k) if n4 > 0 else 1    
        
        if n2 > 0:
            flg = 1 if k < 0 else self.checkNumAll([a, b]) 
        else:
            flg = 1 if k < 0 else self.checkNumAll([a]) 
        
        return flg    


class r_1_2(Reaction):
    
    def __init__(self, name, n1, a, p, n3, x, n4, y):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, p, n3, x, n4, y)       
        
    def react(self): 
        p = self.p
        k = self.getK1(self.a, p)
        flg = self.update(self.n1, self.a, 0, None, k, self.n3, self.x, self.n4, self.y)
        while(flg == 0):
            print("while roop in one_two : ", "flg = ", flg)
            flg = self.update(self.n1, self.a, 0, None, -k, self.n3, self.x, self.n4, self.y)
            p = p * PROB_PARA
            k = self.getK1(self.a, p)
            flg = self.update(self.n1, self.a, 0, None, k, self.n3, self.x, self.n4, self.y)  


class r_1_1(Reaction):
    
    def __init__(self, name, n1, a, p, n3, x):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, p, n3, x, 0, None)           
        
    def react(self): 
        p = self.p
        k = self.getK1(self.a, p)
        flg = self.update(self.n1, self.a, 0, None, k, self.n3, self.x, 0, None)        
        while(flg == 0):
            print("while roop in r_1_1 : ", "flg = ", flg)
            flg = self.update(self.n1, self.a, 0, None, -k, self.n3, self.x, 0, None) 
            p = p * PROB_PARA
            k = self.getK1(self.a, p)
            flg = self.update(self.n1, self.a, 0, None, k, self.n3, self.x, 0, None) 


class r_1_0(Reaction):
    
    def __init__(self, name, n1, a, p):
        super().__init__(name, DUMMY_NUM, n1, a, 0, None, p, 0, None, 0, None)        
        
    def react(self): 
        p = self.p
        k = self.getK1(self.a, p)
        flg = self.update(self.n1, self.a, 0, None, k, 0, None, 0, None)   
        while(flg == 0):
            print("while roop in r_1_0 : ", "flg = ", flg)
            flg = self.update(self.n1, self.a, 0, None, -k, 0, None, 0, None)
            p = p * PROB_PARA
            k = self.getK1(self.a, p)
            flg = self.update(self.n1, self.a, 0, None, k, 0, None, 0, None)


class r_2_1(Reaction):
    
    def __init__(self, name, all, n1, a, n2, b, p, n3, x):
        super().__init__(name, all, n1, a, n2, b, p, n3, x, 0, None)
        
    def react(self):
        p = self.p        
        k = self.getK2(self.a, self.b, p)
        flg = self.update(self.n1, self.a, self.n2, self.b, k, self.n3, self.x, 0, None)
        while(flg == 0):
            print("while roop in r_2_1 : ", "flg = ", flg)
            flg = self.update(self.n1, self.a, self.n2, self.b, -k, self.n3, self.x, 0, None)
            p = p * PROB_PARA
            k = self.getK2(self.a, self.b, p)
            flg = self.update(self.n1, self.a, self.n2, self.b, k, self.n3, self.x, 0, None)


class r_2_2(Reaction):
    
    def __init__(self, name, all, n1, a, n2, b, p, n3, x, n4, y):
        super().__init__(name, all, n1, a, n2, b, p, n3, x, n4, y)     
        
    def react(self):
        p = self.p        
        k = self.getK2(self.a, self.b, p)
        flg = self.update(self.n1, self.a, self.n2, self.b, k, self.n3, self.x, self.n4, self.y)
        while(flg == 0):
            print("while roop in r_2_2 : ", "flg = ", flg)
            flg = self.update(self.n1, self.a, self.n2, self.b, -k, self.n3, self.x, self.n4, self.y)
            p = p * PROB_PARA
            k = self.getK2(self.a, self.b, p)
            flg = self.update(self.n1, self.a, self.n2, self.b, k, self.n3, self.x, self.n4, self.y)
            

class allReaction:
    
    def __init__(self): 
        self.allReactions = {}
        self.all = 0

    def setReaction(self, ls, elem):
        className = ls[0].strip()
        rn = ls[0].strip() + '_' + ls[1].strip()
        
        if   className == "r1_0":
            self.allReactions[rn] = r_1_0(rn, int(ls[2]), elem[ls[3].strip()], float(ls[4]))
        
        elif className == "r1_1":
            self.allReactions[rn] = r_1_1( rn, int(ls[2]), elem[ls[3].strip()], float(ls[4]), \
                                          int(ls[5]), elem[ls[6].strip()])
        
        elif className == "r1_2":
            self.allReactions[rn] = r_1_2(rn, int(ls[2]), elem[ls[3].strip()], float(ls[4]), \
                                          int(ls[5]), elem[ls[6].strip()], \
                                              int(ls[7]), elem[ls[8].strip()])

        elif className == "r2_1":
            self.allReactions[rn] = r_2_1(rn, self.all, int(ls[2]), elem[ls[3].strip()], \
                                          int(ls[4]), elem[ls[5].strip()], float(ls[6]), \
                                              int(ls[7]), elem[ls[8].strip()])
        
        elif className == "r2_2":
            self.allReactions[rn] = r_2_2(rn, self.all, int(ls[2]), elem[ls[3].strip()], \
                                          int(ls[4]), elem[ls[5].strip()], float(ls[6]), \
                                              int(ls[7]), elem[ls[8].strip()], \
                                                  int(ls[9]), elem[ls[10].strip()])
        
        else:
            pass





















        
            
        
        
        
        
        