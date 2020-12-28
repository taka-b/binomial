# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:39:10 2019

@author: Takashi Sato
"""

import reaction as rc
import element as ce
import utility as ut



time = []

elms = ce.allElements()
reacs = rc.allReaction()
utils = ut.Utility()

TimeDataPrint = "ON"
path = 'inp_Glycolysis_05_05.txt'
# path = 'inp_004_04.txt'

with open(path) as f:
    s = f.read()
    print(s)
    
with open(path) as f:
    flg_01 = 0
    elementCount = 0
    elementNum = 0
    reactionCount = 0
    reactionNum = 0
    plotCount = 0
    plotNum = 0
    l = f.readlines()
    
    for line in l:
        print("")
        line_new = line.replace('\n','')
        line_sprit = [x.strip() for x in line_new.split(",")]
        
        print(line_sprit)
        
        if line_sprit[0] == "*Time" :
            t0 = int(line_sprit[1])
            t1 = int(line_sprit[2])
            time = [t for t in range(t0, t1)]
            printTime = int(line_sprit[3])
      
        # Set all elements with name, initial number, and color for plot
        if flg_01 == 1 and elementCount < elementNum:
            elms.setElement(line_sprit)
            elementCount += 1
        
        # Set all reactions reaction name, reaction type, and reaction rate
        if flg_01 == 2 and reactionCount < reactionNum:
            reacs.setReaction(line_sprit, elms.allElements)
            reactionCount += 1
            
        if flg_01 == 3 and plotCount < plotNum:
            utils.appendList(line_sprit, elms.allElements)
            plotCount += 1

        if   line_sprit[0] == "*Element" :
            elementNum = int(line_sprit[1])  
            flg_01 = 1
        elif line_sprit[0] == "*Element End" :
            flg_01 = 0
        
        elif line_sprit[0] == "*Reaction" :
            reactionNum = int(line_sprit[1])
            reacs.all = int(line_sprit[2])
            flg_01 = 2
        elif line_sprit[0] == "*Reaction End" :
            flg_01 = 0
        
        elif line_sprit[0] == "*Plot" :
            plotNum = int(line_sprit[1])
            flg_01 = 3
        elif line_sprit[0] == "*Plot End" :
            flg_01 = 0
                   
        print( f"flg_01 {flg_01} open." )


for t in range(t0+1, t1) :
    
    for re in reacs.allReactions.values():
        re.react()
    
    if TimeDataPrint == "ON" and t%printTime == 0 :
        num = [elem.n for elem in elms.allElements.values() ]
        print( f"Time :{t:8},      Numbers of elements :   ") 
        print("      " , num)
        
    for el in elms.allElements.values():
        el.updateNumbers()
    

utils.plotAll(time)



