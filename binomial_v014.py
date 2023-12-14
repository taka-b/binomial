# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:39:10 2019

@author: Takashi Sato

Complex Reaction System Laboratory
    
Copyright (c) 2022 Takashi Sato
    
This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/

"""

# from binomial_167.py

import element_31 as ce
import reaction_42 as rc
import utility_41 as ut
import reactionManage_04 as rm
import polymer_11 as po
import setting_06 as se
import os, sys
import time, datetime
import random

elms = ce.allElements()
reacs = rc.allReaction()
timeM = ut.timeManage()
utils = ut.Utility()
creR = rm.createReaction()
poly = po.Polymer()

t1 = time.time()
TimeDataPrint = "YES"
ParameterStudy = "NO"
ShowInSpyder = "YES"
CalculationOrder = " "  # "random" or " "


print(os.getcwd())
os.chdir('..')
print(os.getcwd())
# needs this dummy name
fName = "DUMMY"

'''
You need a input file to run from the Spyder.
'''
# select a input file
# fName = 'inp_bind_001.txt'
# fName = 'inp_bind_002.txt'  
# fName = 'inp_Michaelis–Menten kinetics_003.txt'
# fName = "inp_MWC-allosteric_016.txt"
# fName = "inp_feedback_408.txt"
# fName = "inp_feedforward_010.txt"
# fName = "inp_feedforward_011.txt"
fName = 'inp_SIR_004.txt'
# fName = 'inp_SIR_011.txt'
# fName = 'inp_SIR_012.txt'

# fName = "inp_circadian_013.txt"
# fName = "inp_autocatalytic_111.txt"
# fName = "inp_geneticDrift_130.txt"
# fName = "inp_Lotka-Volterra_506_04.txt"
# fName = 'test_038.txt'
# fName = 'inp_immune_323.txt'
# fName = 'inp_Glycolysis_90.txt'
# fName = "inp_oscillation_010.txt"
# fName = "inp_exponential_402.txt"
    
fName, ShowInSpyder = ut.setFromTerminal(fName, ShowInSpyder)

ut.changeDirectory(fName)

class Binomial:

    def __init__(self):
        self.newFileName = ""
        
    def createNewFile(self, fName):
        self.newFileName = se.createNewFile(fName)

    def openReadFile(self):       
        se.openReadFile(self.newFileName, elms, reacs, timeM, utils, creR, poly)
    
    def preperation(self):
        # 2022.1.3
        for el in elms.InOutElements.values():
            el.calcSchedule(timeM)
        if TimeDataPrint == "YES":
            utils.makeFolder(self.newFileName)
    
    def calculate(self):        
        for step in timeM.allTime:       
            if step in timeM.printTimes:             # 2022.2.12
                aElNames = elms.allElements.keys()
                numE = [elem.n for elem in elms.allElements.values()]
                numR = [reac.rName for reac in reacs.allReactions.values()]
                print()
                print(f" Time ({timeM.unit}) :{step:8} !!!!!!!!!!!!!!!!!!!!!")
                print(" Numbers of Elements :  ", len(numE), "  \n" , numE)
                print(" Names of Elements :  ", "\n" , aElNames)        
                print(" Numbers of reactions :  ", len(numR), "  \n" , numR)           
            # 2022.1.3
            for el in elms.InOutElements.values():
                if step in el.schedule and step != 0:
                    index = el.schedule.index(step)
                    el.n = el.n + el.deltaN[index]
                    if el.n < 0:                                # 2022.9.3
                        el.n = el.n - el.deltaN[index]
            
            reactions = [v for v in reacs.allReactions.values()]
            
            if CalculationOrder == "random":    # 2022.6.22
                random.shuffle(reactions)
            else:
                pass

            for re in reactions:
                re.react()
            for el in elms.allElements.values():
                el.updateNumbers()                     
        
            if step in timeM.plotTimes and step != 0:            # 2022.8.28　ここに移動
                tRange = [t for t in range(timeM.startTime, step + 2)]
                utils.plotSome(tRange, step, timeM.unit, self.newFileName, TimeDataPrint, ShowInSpyder)              
                if "polymer" in self.newFileName:
                    poly.plotDistribution(step, utils, self.newFileName, elms, TimeDataPrint, ShowInSpyder)
        
            if TimeDataPrint == "YES" and step == timeM.endTime:
                print()
                print("Print times: ", timeM.getPrintTimes())
                utils.saveCsvFile(step, timeM.getCsvTimes(), self.newFileName, elms, timeM)
                utils.saveCsvFile_02(step, timeM.getCsvTimes(), self.newFileName, elms, timeM)
                utils.saveCsvFile_03(step, timeM.getCsvTimes(), self.newFileName, reacs, timeM)
    
    def endStep(self):
        t2 = time.time()
        elapsed_time = t2 - t1
        td = datetime.timedelta(seconds=elapsed_time)
        print()
        print(f"Elapsed_time : {td}")
    
    def polymerStep(self):
        if "polymer" in self.newFileName:
            poly.plotMWD_atAnyTime_02(timeM, utils, self.newFileName, elms, TimeDataPrint, poly.getMaxDegrees(elms.polymers), ShowInSpyder)  # 2022.2.11
            poly.calculateMwMn(utils, timeM, self.newFileName, elms, TimeDataPrint)
            poly.saveDistribution(utils, timeM, self.newFileName)
            poly.plotMwMn(utils, timeM, self.newFileName, ShowInSpyder)
 
    
# create Binomial object
bi = Binomial()

# for a special input file with *set 
bi.createNewFile(fName)

# temporal
# sys.exit()

# run a calculation
bi.openReadFile()
bi.preperation()
bi.calculate()
bi.endStep()
bi.polymerStep()
