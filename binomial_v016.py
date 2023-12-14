# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:39:10 2019

@author: Takashi Sato

Complex Reaction System Laboratory

Copyright (c) 2022 Takashi Sato
    
This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/

made from binomial_200.py
"""

import os
import time
import datetime
import random
import element_35 as ce
import reaction_63 as rc
import utility_55 as ut
import setting_30 as se
import polymer_12 as po
import setManage_01 as sm
import utility_functions as uf


json_file = "binomial_parameters_02.json"

# Select a input file.
# input_file = "inp_bind_001.txt"    
# input_file = "inp_bind_002.txt"  
# input_file = "inp_feedback_408.txt"
# input_file = "inp_feedforward_010.txt"
# input_file = "inp_feedforward_011.txt"
# input_file = "inp_Michaelis_Menten kinetics_003.txt"
# input_file = "inp_SIR_010.txt"
# input_file = "inp_SIR_011.txt"
# input_file = "inp_SIR_012.txt"
# input_file = "inp_immune_323.txt"
# input_file = "test_059.txt"

# Use Linux version Python for calculationg
# input_file = "H2O_007.txt"
# input_file = "H2O_008.txt"
# input_file = "inp_MWC-allosteric_016.txt"
# input_file = "inp_MWC-allosteric_016_02.txt"

input_file = "Set_H+Na+_029.txt"



def change_directory_to_inputFile(filename):
    os.chdir('..')
    uf.changeDirectory_to_inputFile(filename)

def main(input_file):
    ut.init(json_file)
    
    all_elements = ce.AllElements()
    all_reactions = rc.reactions()
    timeM = ut.TimeManage()
    utils = ut.Utility()
    all_plot = ut.AllPlots()
    poly = po.Polymer()
    all_set = sm.allSets()

    start_time = time.time()
    CSV_OUTPUT = ut.CSV_OUTPUT
    FIG_OUTPUT = ut.FIG_OUTPUT
    RestartFile = ut.RestartFile
    ShowFigure = "YES"
    MAX_WORKERS = None  # process numbers (int). None is default, choosing suitable numbers.
    
    rc.set_Json_item(ut.EntropyCalc)
    input_file, ShowFigure = uf.setFromTerminal(input_file, ShowFigure)
    change_directory_to_inputFile(input_file)

    bi = Binomial(all_elements, all_reactions, timeM, utils, all_plot, poly, all_set, MAX_WORKERS)
    bi.createNewFile(input_file)
    bi.openReadFile()
    bi.setDefine()
    bi.preparation(CSV_OUTPUT, FIG_OUTPUT)
    bi.calculate(CSV_OUTPUT, ShowFigure, MAX_WORKERS)
    bi.restart_File(RestartFile)
    bi.end_step(start_time)
    bi.polymer_step(CSV_OUTPUT, ShowFigure)


class Binomial:

    def __init__(self, all_elements, all_reactions, timeM, utils, all_plot, poly, all_set, MAX_WORKERS):
        self.all_elements = all_elements
        self.all_reactions = all_reactions
        self.timeM = timeM
        self.utils = utils
        self.all_plot = all_plot
        self.poly = poly
        self.all_set = all_set
        self.newFileName = ""
        self.reactFunc =[]           # separated by independent react()

    def createNewFile(self, fName):
        self.newFileName = se.createNewFile(fName)

    def openReadFile(self):
        se.openReadFile(self.newFileName, self.all_elements, self.all_reactions,
                        self.timeM, self.utils, self.poly, self.all_plot)
        
    def setDefine(self):
        se.setDefine(self.newFileName, self.all_elements, self.all_reactions, self.all_plot, self.all_set)

    def preparation(self, CSV_OUTPUT, FIG_OUTPUT):
        for el in self.all_elements.InOutElements.values():
            el.calcSchedule(self.timeM)
        if CSV_OUTPUT == "YES" or FIG_OUTPUT == "YES":
            self.utils.makeFolder(self.newFileName)
        
    def makeReactionsSet(self):
        self.all_reactions.separate_independent_reactions()
        reactions = self.all_reactions.independent_Reaction_sets     # separated by independent reactions
        self.reactFunc = [[self.all_reactions.reactions[re].react() for re in re_ind] for re_ind in reactions]

    def calculate(self, CSV_OUTPUT, ShowFigure, MAX_WORKERS):
        for step in self.timeM.allTime:
            self.print_info(step)
            self._update_elements(step)
            self._perform_reactions()
            self.update_numbers()
            self.plot_results(step, CSV_OUTPUT, ShowFigure)
            if CSV_OUTPUT == "YES" and step == self.timeM.endTime:
                self.save_csv_output(step, CSV_OUTPUT)

    def print_info(self, step):
        if step in self.timeM.printTimes:
            numE = [elem.n for elem in self.all_elements.elements.values()]
            numR = [reac.reactionName for reac in self.all_reactions.reactions.values()]
            print()
            print(f" Time ({self.timeM.unit}) :{step:8} !!!!!!!!!!!!!!!!!!!!!")
            print(" Numbers of Elements :  ", len(numE))
            print(" Numbers of reactions :  ", len(numR))

    def _update_elements(self, step):
        for el in self.all_elements.InOutElements.values():
            if step in el.schedule and step != 0:
                index = el.schedule.index(step)
                el.n = el.n + el.deltaN[index]
                if el.n < 0:
                    el.n = el.n - el.deltaN[index]

    def _perform_reactions(self):
        reactions = [v for v in self.all_reactions.reactions.values()]
        random.shuffle(reactions)
        for re in reactions:
            re.react()

    def update_numbers(self):
        for el in self.all_elements.elements.values():
            el.updateNumbers()

    def plot_results(self, step, CSV_OUTPUT, ShowFigure):
        if step in self.timeM.plotTimes and step != 0:
            tRange = [t for t in range(self.timeM.startTime, step + 2)]
            self.all_plot.plotAllElements(tRange,
                                       step,
                                       self.timeM.unit,
                                       self.newFileName,
                                       ShowFigure,
                                       self.utils)
            if "polymer" in self.newFileName:
                self.poly.plotDistribution(step,
                                           self.utils,
                                           self.newFileName,
                                           self.all_elements,
                                           CSV_OUTPUT,
                                           ShowFigure)

    def save_csv_output(self, step, CSV_OUTPUT):
        print()
        print("CSV_OUTPUT: ", CSV_OUTPUT)
        print("Print times: ", self.timeM.getPrintTimes())
        os.chdir(self.utils.resultFolder)
        self.utils.saveCsvFile(step, self.timeM.getCsvTimes(), self.newFileName, self.all_elements, self.timeM)
        self.utils.saveCsvFile_02(step, self.timeM.getCsvTimes(), self.newFileName, self.all_elements, self.timeM)
        self.utils.saveCsvFile_03(step, self.timeM.getCsvTimes(), self.newFileName, self.all_reactions, self.timeM)
        
    def restart_File(self, RestartFile):
        if RestartFile == "YES":
            se.writeRestartFile(self.newFileName, self.all_elements)

    def end_step(self, start_time):
        elapsed_time = time.time() - start_time
        td = datetime.timedelta(seconds=elapsed_time)
        print()
        print(f"Elapsed_time : {td}")

    def polymer_step(self, CSV_OUTPUT, ShowFigure):
        if "polymer" in self.newFileName:
            self.poly.plotMWD_atAnyTime_02(self.timeM,
                                           self.utils,
                                           self.newFileName,
                                           self.all_elements,
                                           CSV_OUTPUT,
                                           self.poly.getMaxDegrees(self.all_elements.polymers),
                                           ShowFigure)
            self.poly.calculateMwMn(self.utils, self.timeM, self.newFileName, self.all_elements, CSV_OUTPUT)
            self.poly.saveDistribution(self.utils, self.timeM, self.newFileName)
            self.poly.plotMwMn(self.utils, self.timeM,self.newFileName, ShowFigure)

if __name__ == "__main__":
    main(input_file)
