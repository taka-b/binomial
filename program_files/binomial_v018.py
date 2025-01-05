# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:39:10 2019

@author: Takashi Sato

Complex Reaction System Laboratory

Copyright (c) 2022- Takashi Sato
    
This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/

based on binomial_230.py Jan 1 2025
"""

import os
import time
import datetime
import random
import element_41 as ce
import reaction_77 as rc
import utility_69 as ut
import setting_35 as se
import polymer_13 as po
import setManage_02 as sm
import utility_functions_02 as uf   # utility_functions_02 is also used in reaction_xx.py, element_xx.py and utility_xx.py 

json_file = "binomial_parameters_07.json"


# In input_files_01
input_file = "H2O_007.txt"
# input_file = "H2O_008.txt"
# input_file = "inp_bind_001.txt"
# input_file = "inp_bind_002.txt"   
# input_file = "inp_feedback_408.txt" 
# input_file = "inp_feedforward_010.txt"
# input_file = "inp_feedforward_011.txt"
# input_file = "inp_Michaelis_Menten kinetics_003.txt"
# for Linux
# input_file = "inp_MWC-allosteric_016.txt"

# In input_files_02
# input_file = "inp_autocatalytic_111.txt"
# input_file = "inp_exponential_401.txt"
# input_file = "inp_geneticDrift_130.txt"
# input_file = "inp_Glycolysis_115.txt"
# input_file = "inp_immune_323.txt"
# input_file = "inp_oscillation_010.txt"
# input_file = "inp_SIR_010.txt"
# input_file = "test_059.txt"

# In input_files_03
# input_file = "Set_401.txt"
# input_file = "Set_membrane_004_10.txt" 
input_file = "System-3.txt"         
# input_file = "System-6.txt"  
# input_file = "System-8.txt"                         
# for Linux
# input_file = "Set_cell_mito_527.txt"
    
# In input_files_04
# input_file = "Channel_pump_007.txt"
# input_file = "Lotka-Volterra_211_034_03.txt"
# for Linux
# input_file = "phosphate_032.txt" 

def change_directory_to_inputFile(filename):
    os.chdir('..')
    uf.changeDirectory_to_inputFile(filename)

def main(input_file):
    # "Preparation"
    start_time = time.time()
    ut.json_init(json_file)
    all_elements = ce.AllElements()
    all_reactions = rc.reactions()
    timeM = ut.TimeManage()
    utils = ut.Utility()
    all_plots = ut.AllPlots()
    poly = po.Polymer()
    all_set = sm.allSets()

    print("\n !!! New calculation starts. !!! \n")
    RestartFile = ut.RestartFile
    RestartFile_period = ut.RestartFile_period
    print("RestartFile_period: ", RestartFile_period)     # 2023.11.26
    ShowFigure = "YES"

    rc.set_Json_item(ut.EntropyCalc, ut.InformationCalc, ut.n_p_Binomial)
    input_file, ShowFigure = uf.setFromTerminal(input_file, ShowFigure)
    change_directory_to_inputFile(input_file)
    
    # Main object for calculation
    bi = Binomial(all_elements, all_reactions, timeM, utils, all_plots, poly, all_set)
    bi.createNewFile(input_file)
    bi.openReadFile()
    bi.setDefine()
    bi.preparation()
    bi.calculate(ShowFigure)
    bi.restart_File(RestartFile)
    bi.polymer_step(ShowFigure)
    bi.end_step(start_time)


class Binomial:

    def __init__(self, all_elements, all_reactions, timeM, utils, all_plots, poly, all_set):
        self.all_elements = all_elements
        self.all_reactions = all_reactions
        self.timeM = timeM
        self.utils = utils
        self.all_plots = all_plots
        self.poly = poly
        self.all_set = all_set
        self.newFileName = ""
        self.reactFunc =[]           # separated by independent react()

    def createNewFile(self, fName):
        self.newFileName = se.createNewFile(fName)

    def openReadFile(self):
        se.openReadFile(self.newFileName, self.all_elements, self.all_reactions,
                        self.timeM, self.utils, self.poly, self.all_plots)
        
    def setDefine(self):
        se.setDefine(self.newFileName, self.all_elements, self.all_reactions, self.all_plots, self.all_set)

    def preparation(self):
        for el in self.all_elements.InOutElements.values():
            el.calcSchedule(self.timeM)
        if ut.Make_folder == "YES" :
            self.utils.makeFolder(self.newFileName)

    def calculate(self, ShowFigure):
        for step in self.timeM.allTime:
            self.print_info(step)
            self._perform_reactions()      # 2023.11.26 change the order 
            self._update_elements(step)     # 2023.11.26 change the order
            self._update_numbers()            # 2024.2.11 
            
            if ut.FIG_OUTPUT == "YES" and step+1 in self.timeM.getCsvTimes():
                self.utils.saveDataForPlots(step, self.all_elements)
            
            if step in self.timeM.plotTimes and step != self.timeM.startTime:
                self.plot_results(step, ShowFigure)

            if ut.CSV_OUTPUT == "YES" and step+1 in self.timeM.getCsvTimes():
                self.utils.saveDataForCSV(step, self.all_elements)   
            
            if ut.Make_folder == "YES" and step == self.timeM.endTime:    
                self._save_csv_output_001()

    def print_info(self, step):
        if step in self.timeM.getPrintTimes():
            numE = [elem.n for elem in self.all_elements.elements.values()]
            numR = [reac.reactionName for reac in self.all_reactions.reactions.values()]
            print()
            print(f" Time ({self.timeM.unit}) :{step:8} !!!!!!!!!!!!!!!!!!!!!")
            print(" Number of elements :  ", len(numE))
            print(" Number of reactions :  ", len(numR))

    def _update_elements(self, step):
        for el in self.all_elements.InOutElements.values():
            if step in el.schedule and step != self.timeM.startTime:
                index = el.schedule.index(step)
                el.n = el.n + el.deltaN[index]
                if el.n < 0:
                    el.n = el.n - el.deltaN[index]

    def _perform_reactions(self):
        reactions = [v for v in self.all_reactions.reactions.values()]
        random.shuffle(reactions)
        for re in reactions:
            re.react()

    def _update_numbers(self):
        for el in self.all_elements.elements.values():
            el.updateNumbers()

    def plot_results(self, step, ShowFigure):
        # if step in self.timeM.plotTimes and step != self.timeM.startTime:
            print("In plot_results")
            self.all_plots.plotAllElements(self.timeM,
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
                                           ut.FIG_OUTPUT,
                                           ShowFigure)

    def _save_csv_output_001(self):    # 2024.12.29
        os.chdir(self.utils.resultFolder)
        if ut.CSV_OUTPUT == "YES":
            self.utils.saveCsvFile_001(self.timeM.getCsvTimes(), self.newFileName, self.all_elements)
            self.utils.saveCsvFile_002(self.timeM.getCsvTimes(), self.newFileName, self.all_elements)  
        if ut.InformationCalc == "YES" or ut.EntropyCalc == "YES":
            self.utils.saveCsvFile_003(self.newFileName, self.all_reactions, self.timeM)
        if ut.n_p_Binomial == "YES" :
            self.utils.saveCsvFile_004(self.newFileName, self.all_reactions, self.timeM)

    def restart_File(self, RestartFile):
        if RestartFile == "YES":
            se.writeRestartFile(self.newFileName, self.all_elements)

    def end_step(self, start_time):
        elapsed_time = time.time() - start_time
        td = datetime.timedelta(seconds=elapsed_time)
        print()
        print(f"Elapsed_time : {td}")

    def polymer_step(self, ShowFigure):
        if "polymer" in self.newFileName:
            self.poly.plotAndPrintForDist(self.timeM,
                                          self.utils,
                                          self.newFileName,
                                          self.all_elements,
                                          ut.FIG_OUTPUT, 
                                          self.poly.getMaxDegrees(self.all_elements.polymers),
                                          ShowFigure)
            self.poly.calculateMwMn(self.utils, self.timeM, self.newFileName, self.all_elements, ut.CSV_OUTPUT)
            self.poly.saveDistribution(self.utils, self.timeM, self.newFileName)
            self.poly.plotMwMn(self.utils, self.timeM,self.newFileName, ShowFigure)

if __name__ == "__main__":
    main(input_file)
