# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:39:10 2019

@author: Takashi Sato

Complex Reaction System Laboratory

Copyright (c) 2022- Takashi Sato
    
This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/

"""

import os
import time
import datetime
import random
import element_43 as ce
import reaction_83 as rc
import utility_75 as ut
import setting_39 as se
import polymer_13 as po
import setManage_04 as sm
# Note: The "utility_functions" module is also used in other modules such as reaction_xx.py, element_xx.py, and utility_xx.py.
# If you decide to rename this module, make sure to update the import statements in all dependent modules accordingly.
import utility_functions as uf 

json_file = "binomial_parameters_11.json"

# from reactions import perform_reactions
# input_file = "System-3.txt"
# input_file = "gpt_glycolysis_04.txt"Z
# input_file = "particle_205_10.txt"
# input_file = "inp_bind_002.txt"
# input_file = "cancer_028_25.txt"                    # 2025.3.5
# input_file = "Logistic_test15_06.txt"          
# input_file = "Set_cell_mito_543.txt"                          # 2024.1.21
# input_file = "Set_polyamine_073_o19_best.txt"                         # 2024.10.3
# input_file = "amino_pool_02.txt"                         # 2024.10.3
# input_file = "cardiac_014_07.txt"                             # 2024.1.31
# input_file = "Set_Ecoli_008.txt"                              # 2024.5.5
# input_file = "Cell_015.txt"                                   # 2024.7.28
# input_file = "Logistic_test08_11_8.txt"
# input_file = "Set_Ecoli_ploliferation_010.txt"                # 2024.6.2
# input_file = "membrane_2025_016.txt"
# input_file = "Set_414.txt"                               # 2025.1.8
# input_file = "phosphate_032.txt"                              # 2023.6.12
# input_file = "nurve_001.txt"                             # 2025.1.8
# input_file = "inp_exponential_118.txt"           # 2025.4.3

# input_file = "earth_018_for_paper.txt"
# input_file = "inp_feedback_408.txt"
# input_file = "inp_feedforward_011.txt"
# input_file = "Set_test_A_24.txt"
# input_file = "human_306.txt"       
# input_file = "inp_immune_323.txt"
# input_file = "inp_circadian_026.txt"
# input_file = "Set_polyamine_063_o10_best1.txt"
# input_file = "Lotka-Volterra_623_27.txt"
# input_file = "inp_polymer_237.txt"
# input_file = "inp_autocatalytic_111.txt"
input_file = "figure_4A_35_30.txt"

# Use Linux version Python for calculationg
# input_file = "inp_bind_002.txt"
# input_file = "H2O_007.txt"
# input_file = "inp_Michaelis_Menten_kinetics_003.txt"
# input_file = "inp_MWC-allosteric_016_02.txt"
# input_file = "inp_virus_100.txt"
# input_file = "Set_cell_mito_517.txt"
# input_file = "Channel_007_04.txt"
# input_file = "Channel_pump_005.txt"
# input_file = "Channel_pump_007.txt"
# input_file = "Set_cell_Lacto_005.txt"
# input_file = "inp_SIR_012_03.txt"
# input_file = "test_060.txt"

def change_directory_to_inputFile(filename):
    os.chdir('..')
    uf.changeDirectory_to_inputFile(filename)

def main(input_file):
    # "Preparation"
    start_time = time.time()
    ut.json_init(json_file)
    allElements = ce.AllElements()
    allReactions = rc.AllReactions()
    timeM = ut.TimeManage()
    utils = ut.Utility()
    allPlots = ut.AllPlots()
    poly = po.Polymer()
    allSets = sm.allSets()

    RestartFile = ut.RestartFile
    RestartFile_period = ut.RestartFile_period
    print("RestartFile_period: ", RestartFile_period)     # 2023.11.26
    ShowFigure = "YES"

    rc.set_Json_item(ut.EntropyCalc, ut.InformationCalc, ut.n_p_Binomial)
    input_file, ShowFigure = uf.setFromTerminal(input_file, ShowFigure)
    change_directory_to_inputFile(input_file)
    
    print("\n !!! New calculation starts. !!!")
    print(f" !!! File name is {input_file}. !!! \n")
    
    # Main object for calculation
    bi = Binomial(allElements, allReactions, timeM, utils, allPlots, poly, allSets)
    bi.createNewFile(input_file)
    bi.openReadFile()
    bi.setDefine()
    bi.preparation()
    bi.calculate(ShowFigure)
    bi.restart_File(RestartFile)
    bi.polymer_step(ShowFigure)
    bi.end_step(start_time)
    


class Binomial:

    def __init__(self, allElements, allReactions, timeM, utils, allPlots, poly, allSets):
        self.allElements = allElements
        self.allReactions = allReactions
        self.timeM = timeM
        self.utils = utils
        self.allPlots = allPlots
        self.poly = poly
        self.allSets = allSets
        self.newFileName = ""
        self.reactFunc =[]           # separated by independent react()

    def createNewFile(self, fName):
        self.newFileName = se.createNewFile(fName)

    def openReadFile(self):
        # 2025.1.8
        se.openReadFile(self.newFileName, self.allElements, self.allReactions,
                        self.timeM, self.utils, self.poly, self.allPlots, self.allSets)
        
    def setDefine(self):
        se.setDefine(self.newFileName, self.allElements, self.allReactions, self.allPlots, self.allSets)

    def preparation(self):
        for el in self.allElements.InOutElements.values():
            el.calcSchedule(self.timeM)
        if ut.Make_folder == "YES" :
            self.utils.makeFolder(self.newFileName)

    def calculate(self, ShowFigure):
        for step in self.timeM.allTime:
            self.print_info(step)
            self._perform_reactions()      # 2023.11.26 change the order 
            self._update_elements(step)     # 2023.11.26 change the order
            self._update_numbers()            # 2024.2.11 
            
            # if ut.FIG_OUTPUT == "YES" and step+1 in self.timeM.getCsvTimes():    # 2025.2.2
            if ut.FIG_OUTPUT == "YES" and step in self.timeM.getCsvTimes():
                if self.timeM.endTime == step:
                    pass
                else:
                    self.utils.saveDataForPlots(step, self.allElements)
            
            if step in self.timeM.plotTimes and step != self.timeM.startTime:
                self.plot_results(step, ShowFigure)

            # if ut.CSV_OUTPUT == "YES" and step+1 in self.timeM.getCsvTimes():    # 2025.2.2
            if ut.CSV_OUTPUT == "YES" and step in self.timeM.getCsvTimes():
                self.utils.saveDataForCSV(step, self.allElements)   
            
            if ut.Make_folder == "YES" and step == self.timeM.endTime:    
                self._save_csv_output_001()

    def print_info(self, step):
        if step in self.timeM.getPrintTimes():
            numE = [elem.n for elem in self.allElements.elements.values()]
            numR = [reac.reactionName for reac in self.allReactions.reactions.values()]
            print()
            print(f" Time ({self.timeM.unit}) :{step:8} !!!!!!!!!!!!!!!!!!!!!")
            print(" Number of elements :  ", len(numE))
            print(" Number of reactions :  ", len(numR))

    def _perform_reactions(self):
        reactions = [v for v in self.allReactions.reactions.values()]
        if ut.Reaction_Order == "random":
            random.shuffle(reactions)
        for re in reactions:
            re.react()

    def _update_elements(self, step):
        for el in self.allElements.InOutElements.values():
            # if step in el.schedule and step != self.timeM.startTime:    # 2025.2.2
            if step in el.schedule:
                index = el.schedule.index(step)
                el.n = el.n + el.deltaN[index]
                if el.n < 0:
                    el.n = el.n - el.deltaN[index]

    def _update_numbers(self):
        for el in self.allElements.elements.values():
            el.updateNumbers()

    def plot_results(self, step, ShowFigure):
        # if step in self.timeM.plotTimes and step != self.timeM.startTime:
            print("In plot_results")
            self.allPlots.plotAllElements(self.timeM,
                                           step,
                                           self.timeM.unit,
                                           self.newFileName,
                                           ShowFigure,
                                           self.utils)
            if "polymer" in self.newFileName:
                self.poly.plotDistribution(step,
                                           self.utils,
                                           self.newFileName,
                                           self.allElements,
                                           ut.FIG_OUTPUT,
                                           ShowFigure)

    def _save_csv_output_001(self):    # 2024.12.29
        os.chdir(self.utils.resultFolder)
        if ut.CSV_OUTPUT == "YES":
            self.utils.saveCsvFile_001(self.timeM.getCsvTimes(), self.newFileName, self.allElements)
            self.utils.saveCsvFile_002(self.timeM.getCsvTimes(), self.newFileName, self.allElements)  
        if ut.InformationCalc == "YES" or ut.EntropyCalc == "YES":
            self.utils.saveCsvFile_003(self.newFileName, self.allReactions, self.timeM)
        if ut.n_p_Binomial == "YES" :
            self.utils.saveCsvFile_004(self.newFileName, self.allReactions, self.timeM)

    def restart_File(self, RestartFile):
        if RestartFile == "YES":
            # uf.writeRestartFile(self.newFileName, self.allElements)
            uf.writeRestartFile_new7(self.newFileName, self.allElements)
            # uf.compareRestartFileWithObjects(new_restart_file_name, self.allElements, self.allReactions, self.allPlots)

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
                                          self.allElements,
                                          ut.FIG_OUTPUT, 
                                          self.poly.getMaxDegrees(self.allElements.polymers),
                                          ShowFigure)
            self.poly.calculateMwMn(self.utils, self.timeM, self.newFileName, self.allElements, ut.CSV_OUTPUT)
            self.poly.saveDistribution(self.utils, self.timeM, self.newFileName)
            self.poly.plotMwMn(self.utils, self.timeM,self.newFileName, ShowFigure)

if __name__ == "__main__":
    main(input_file)
