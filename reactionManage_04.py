#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 11:35:34 2021

@author: takashi
"""
import sys
import random
import collections


class CountMR:
    
    def __init__(self):
        self.reactionMultiCount = 0

    def getReactionMultiCount(self):
        self.reactionMultiCount += 1
        return self.reactionMultiCount


count = CountMR()      # global counter


class createReaction:
    
    def __init__(self):
        self.allreactionATT = []     

        
    def createReactionInProcess(self, time):
        for rA in self.allreactionATT:
            for tp in rA.tParas:    
                if time == tp:
                    print()
                    print(f"!!!! Time :{time:8} !!!!!!!!!!!!!!!!!!!!!")
                    self.createReactions(rA.lsFrom2, rA.elms, rA.reacs)                    

             
    def getBeforeElem(self, beforeElNum, elms):
        # 今の所反応次数は、すべて１とする   # [[n1, el_b1],[n2, el_b2], --- ]
        els = []
        cat = []
        selectAutoKeys = random.sample(elms.autoElements.keys(), beforeElNum)
        selectCatKeys = random.sample(elms.catalyses.keys(), 1)
        els = self.appendReactUnit(selectAutoKeys, elms.autoElements)
        cat = self.appendReactUnit(selectCatKeys, elms.catalyses)           
        return els, cat

    def appendReactUnit(self, selectAutoKeys, elements):     
        e = []
        for k in selectAutoKeys:
            e.append([1, elements[k]])        # 1 は、反応次数　⇒　後に変更！　2021.4.29
        return e

    def getAfterElem(self, beforeElems, afterElNum, elms):
        basics = []
        aNames = []
        afterElems = []
        for e in beforeElems:                    # ここで１文字の名前が入るバグ　2021.6.6
            name = e[1].name
            # print(name)
            basic = self.separateToBasic(name)
            basics.extend(basic)
        # print(f" basics = {basics} ")
        afterElesSet = self.makeAfter(basics, afterElNum)
        # print(f" afterElesSet = {afterElesSet} ")
        aNames = self.returnNames(afterElesSet)
        # print(f" afterNames = {aNames} ")
        self.createElem(aNames, elms)
        # afterElems = self.appendReactUnit(self, aNames, elms.allElements)
        return self.appendReactUnit(aNames, elms.allElements)
        
    # conbert to basic elements
    def separateToBasic(self, name):
        print("name is ", name)
        bel = []
        ch2 = [(s.split("=")[0], int(s.split("=")[1])) for s in name.split("_")]
        print("ch2 is ", ch2)        

        for i, beln in enumerate(ch2):       
            [bel.append(beln[0]) for i in range(beln[1])]      
        # print(f" bel = {bel} ") 
        
        return bel

    def makeAfter(self, bels, afterElNum):    
        random.shuffle(bels)
        # print(f" bels = {bels} ")
        afterList = []
        if len(bels) < afterElNum:
            afterElNum = len(bels)
        nsn = self.rand_ints_nodup(1, len(bels)-1, afterElNum-1)
        nsn.insert(0, 0)
        nsn.append(len(bels))
        # print(f" nsn = {nsn} ")
        
        for i in range(afterElNum):
            afterList.append(bels[nsn[i]:nsn[i+1]])
        
        return afterList

    # non duplicate
    def rand_ints_nodup(self, a, b, k):        
        ns = []
        if b < k:
            k = b
        while len(ns) < k:
            n = random.randint(a, b)
            # print(f" n = {n},  len[ns] = {len(ns)} ")
            if not n in ns:
                ns.append(n)
        # print(f" ns = {ns} ")
        return sorted(ns) 
        
    def returnNames(self, afterList):           
        getEl = []
        for i, els in enumerate(afterList):
            selectDic = dict(collections.Counter(els))  
            getEl.append(selectDic) 
        
        elNames = []
        for el in getEl:
            name = ""
            for k , v in el.items():
                name += k + "=" + str(v) + "_"
            name = name[:-1]
            elNames.append(name)
        # print(f" elNames = {elNames} ")    
        
        return elNames
        
    def createElem(self, aNames, elms):
        for el in aNames:
            elms.setElementFromUtility(el)
    
    def createReactionPolymer(self, ls, elms, reacs):
        # if ls[3] == "M=*_R" and ls[5] == "M":
        if ls[0] == "rP_elong":
            for el, el_obj in elms.allElements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees + int(ls[4])
                    after = self.getAfterPolymer("M=*_R", deg, elms)
                    if after != "":
                        ls1 = ["r2_1", ls[1]+"_"+str(el_obj.degrees), ls[2], el, ls[4], ls[5]]
                        ls2 = [ls[6], reacs.all]
                        ls3 = [ls[7], after]
                        reacs.setReactionMulti(ls1, ls2, ls3, elms.allElements)      
        # elif ls[3] == "M=*_R" and ls[5] == "M=*_R":
        elif ls[0] == "rP_termi":
            for el_1, el_obj_1 in elms.polymers.items():
                deg_1 = el_obj_1.degrees
                for el_2, el_obj_2 in elms.polymers.items():
                    deg_2 = el_obj_2.degrees
                    if el_obj_1.type == "M=*_R" and el_obj_2.type == "M=*_R" and deg_1 <= deg_2:
                         deg = deg_1 + deg_2
                         after = self.getAfterPolymer("M=*", deg, elms)
                         if after != "":
                             ls1 = ["r2_1", ls[1]+"_"+str(deg_1) + "+" + str(deg_2), ls[2], el_1, ls[4], el_2]
                             ls2 = [ls[6], reacs.all]
                             ls3 = [ls[7], after]
                             reacs.setReactionMulti(ls1, ls2, ls3, elms.polymers)  
        elif ls[0] == "rP_trans":
            print("in rP_trans")
            for el, el_obj in elms.allElements.items():
                if el_obj.type == "M=*_R":
                    deg = el_obj.degrees
                    after = self.getAfterPolymer("M=*", deg, elms)
                    print("after element: ", after)
                    if after != "":
                        ls1 = ["r3_3", ls[1]+"_"+str(deg), ls[2], el, ls[4], ls[5], ls[6], ls[7]]
                        ls2 = [ls[8], reacs.all]
                        ls3 = [ls[9], after, ls[11], ls[12], ls[13], ls[14]]
                        print(ls1, ls2, ls3)
                        reacs.setReactionMulti(ls1, ls2, ls3, elms.allElements)  
        else:
            # This code should go to Polymer class.
            print()
            print("***  Error  ***")
            print("Use \"M\" for monomer in Polymerization process!!")
            sys.exit()
                             
    def getAfterPolymer(self, pType, deg, elms):
        rName = ""
        for el, el_obj in elms.polymers.items():
            if el_obj.type == pType and el_obj.degrees == deg:
                rName = el
        return rName
