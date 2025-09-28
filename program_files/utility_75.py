#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:05:35 2020

@author: takashi
"""

import sys, os
import numpy as np
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import datetime
import glob
import json
import math
from scipy.stats import binom
import seaborn as sns
import traceback
import utility_functions as uf


mpl.rcParams['agg.path.chunksize'] = 100000
mpl.rcParams['path.simplify_threshold'] = 0.5

def _load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def json_init(filename):
    
    global config, CSV_OUTPUT, FIG_OUTPUT, RestartFile, Make_folder
    global RestartFile_period, Fig_created_by, Fig_from_CSV, Seaborn_linewidth
    global InformationCalc, EntropyCalc, n_p_Binomial, Optimization 
    global Plot_Legend
    global One_Element_reaction_type
    global Reaction_Order
    
    config = _load_config(filename)
    Make_folder = config["settings"]["making_folder"]   
    InformationCalc = config["settings"]["InformationCalc"]    
    EntropyCalc = config["settings"]["EntropyCalc"]
    n_p_Binomial = config["settings"]["n_p_Binomial"]
    CSV_OUTPUT = config["settings"]["CSV_OUTPUT"]
    FIG_OUTPUT = config["settings"]["FIG_OUTPUT"]
    Fig_from_CSV = config["settings"]["Fig_from_CSV"]
    RestartFile = config["settings"]["RestartFile"]
    RestartFile_period = config["settings"]["RestartFile_period"]
    Fig_created_by = config["settings"]["Matplotlib(1) or Seaborn(2)"]
    Seaborn_linewidth = config["settings"]["Seaborn linewidth"]
    Plot_Legend = config["settings"]["Plot_Legend"] 
    
    Optimization = config["settings_calculation"]["Optimization"]  
    One_Element_reaction_type = config["settings_calculation"]["One-Element-reaction_type"]  
    Reaction_Order = config["settings_calculation"]["Reaction_Order"]   
    
    print("\n Reaction_Order \n")
    # Reaction_Order = config["settings_calculation"]["Reaction_Order"]      
    # Reaction_Order = "random" 
    
    print("EntropyCalc: ", EntropyCalc, ", InformationCalc: ", InformationCalc)

class Plot:
    
    def __init__(self, Plot_Legend):
        self.plotList = []                 # names of elements in one line of the input file
        self.plotScale = ""
        self.title = "Element Number Dynamics"
        self.Plot_Legend = Plot_Legend
        print("self.Plot_Legend", self.Plot_Legend)

    def plotOut_at_aTime():
        pass
    
    def resultsPlot(self, tRange, step, unit, fName, printNum, ShowFigure, utils):   
        print("resultsPlot")
        fig = plt.figure()     
        plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.2)
        for elem in self.plotList:
            if self.Plot_Legend == "YES":
                plt.plot(tRange, elem.plotNumbers, 
                         marker=elem.marker, markersize=4, 
                         label=elem.name, color=elem.color)
            else:
                plt.plot(tRange, elem.plotNumbers, 
                         marker=elem.marker, markersize=4, color=elem.color)
        plt.xlabel(f"Time ({unit})", fontsize=14)
        plt.ylabel("Number (Counts)", fontsize=14)
        plt.yscale(self.plotScale)
        plt.legend(loc='best')
        plt.title(self.title, loc='center',fontsize=14)
           
        if ShowFigure == "YES" and step != 0:  # 2023.3.25
            plt.show()     
        else:
            pass
        if FIG_OUTPUT == "YES" and Optimization == "NO":
            os.chdir(utils.resultFolder)            
            fig.savefig(fName[:-4] + f"_t={format(step, '06')}_{format(printNum, '03')}.png", dpi=200)
        else:
            pass
        plt.clf()
        plt.close()        

    def resultsPlot_02(self, timeM, step, unit, fName, printNum, ShowFigure, utils):
        sns.set(style="whitegrid")  # seabornのスタイルを設定
        fig, ax = plt.subplots()  # seabornはmatplotlibのaxesオブジェクトを利用します
        plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.2)
        tRange = [t for t in range(timeM.startTime, step + 1)]
        for elem in self.plotList:
            # We needs to input elem.currentNums[:-1] because the last calculation will be done for other calculation. 
            if self.Plot_Legend == "YES":
                sns.lineplot(x=tRange, y=elem.currentNums[:-1], label=elem.name, color=elem.color)
            else:
                sns.lineplot(x=tRange, y=elem.currentNums[:-1], color=elem.color)
        ax.set_xlabel(f"Time ({unit})", fontsize=14)
        ax.set_ylabel("Number", fontsize=14)
        ax.set_yscale(self.plotScale)
        plt.legend(loc='best')
        ax.set_title(self.title, loc='center', fontsize=14)
        
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))  # nbinsで目盛りの最大数を指定

        if ShowFigure == "YES" and step != 0:
            plt.show()
        else:
            pass

        if FIG_OUTPUT == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(f"{fName[:-4]}_t={format(step, '06')}_{format(printNum, '03')}.png", dpi=200)

        plt.clf()
        plt.close(fig) 

    def resultsPlot_03(self, tRange, step, unit, fName, printNum, ShowFigure, utils): # 2023.12.2
        sns.set(style="whitegrid")  # seaborn
        fig, ax = plt.subplots()  # seaborn matplotlib axes
        plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.2)
        for elem in self.plotList:            
            print(f"Length of tRange: {len(tRange)}, Length of elem.plotNumbers: {len(elem.plotNumbers)}")
            if self.Plot_Legend == "YES":                                                      
                sns.lineplot(x=tRange, y = elem.plotNumbers, 
                             label = elem.name,
                             color = elem.color,
                             linewidth = Seaborn_linewidth) # 2023.12.2
            else:
                sns.lineplot(x=tRange, y = elem.plotNumbers, 
                             color = elem.color,
                             linewidth = Seaborn_linewidth) # 2023.12.2
        ax.set_xlabel(f"Time ({unit})", fontsize=14)
        ax.set_ylabel("Number", fontsize=14)
        ax.set_yscale(self.plotScale)
        plt.legend(loc='best')
        ax.set_title(self.title, loc='center', fontsize=14)
        
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))  # nbins

        if ShowFigure == "YES" and step != 0:
            plt.show()
        else:
            pass

        if FIG_OUTPUT == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(f"{fName[:-4]}_t={format(step, '06')}_{format(printNum, '03')}.png", dpi=200)

        plt.clf()
        plt.close(fig) 
        
    # def resultsPlot_04(self, tRange, step, unit, fName, printNum, ShowFigure, utils, index): # 2024.4.28
    #     print('FIG_OUTPUT == "YES" and Optimization == "YES"')
    #     sns.set(style="whitegrid")  # seaborn
    #     fig, ax = plt.subplots()  # seaborn matplotlib axes
    #     plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.2)
    #     for elem in self.plotList:
    #         if self.Plot_Legend == "YES": 
    #             sns.lineplot(x=tRange, y = elem.plotNumbers, 
    #                          label = elem.name,
    #                          color = elem.color,
    #                          linewidth = Seaborn_linewidth) # 2023.12.2
    #         else:
    #             sns.lineplot(x=tRange, y = elem.plotNumbers, 
    #                          color = elem.color,
    #                          linewidth = Seaborn_linewidth) # 2023.12.2                
    #     ax.set_xlabel(f"Time ({unit})", fontsize=14)
    #     ax.set_ylabel("Number", fontsize=14)
    #     ax.set_yscale(self.plotScale)
    #     plt.legend(loc='best')
    #     ax.set_title(self.title, loc='center', fontsize=14)
        
    #     os.chdir(utils.resultFolder)  

    #     # Get a list of files matching the pattern
    #     pattern = fName[:-4] + '_*.png'
    #     file_list = glob.glob(pattern)
    #     # Generate the filename
    #     if not file_list:
    #         # If the file list is empty, use the initial filename
    #         file_name = f"{fName[:-4]}_{format(printNum, '03')}_0000000.png"
    #     else:
    #         # If there are existing files, find the highest number and increment it
    #         max_num = 0
    #         for file in file_list:
    #             # Remove the extension from the file name, split by underscore, and get the last part as a number
    #             num = int(os.path.splitext(file)[0].split('_')[-1])
    #             if num > max_num:
    #                 max_num = num
    #         # Generate a new number (add 1 to the existing maximum number)
    #         new_num = max_num + 1
    #         # Format the new file name
            
    #         file_name = f"{fName[:-4]}_{format(printNum, '03')}_{new_num:07d}.png"
    #     # Save the file
    #     fig.savefig(file_name, dpi=200)
    #     plt.clf()
    #     plt.close(fig) 
        

    def resultsPlot_05(self, tRange, step, unit, fName, printNum, ShowFigure, utils, index):  # 2024.4.28
        print('FIG_OUTPUT == "YES" and Optimization == "YES"')
        
        sns.set(style="whitegrid")  # seaborn
        fig, ax = plt.subplots()  # seaborn matplotlib axes
        plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.2)
    
        try:
            # **データが正常かチェック**
            has_valid_data = False
            for elem in self.plotList:
                if elem.plotNumbers is not None and not np.any(np.isnan(elem.plotNumbers)):  # NaNチェック
                    if self.Plot_Legend == "YES":
                        sns.lineplot(x=tRange, y=elem.plotNumbers, 
                                     label=elem.name,
                                     color=elem.color,
                                     linewidth=Seaborn_linewidth)  # 2023.12.2
                    else:
                        sns.lineplot(x=tRange, y=elem.plotNumbers, 
                                     color=elem.color,
                                     linewidth=Seaborn_linewidth)  # 2023.12.2
                    has_valid_data = True                    
            
            # **データが全て無効 (NaN ばかり) ならエラーを発生させる**
            if not has_valid_data:
                raise ValueError("全てのデータが無効（None または NaN）です。")
    
            ax.set_xlabel(f"Time ({unit})", fontsize=14)
            ax.set_ylabel("Number", fontsize=14)
            ax.set_yscale(self.plotScale)
            plt.legend(loc='best')
            ax.set_title(self.title, loc='center', fontsize=14)
    
        except Exception as e:
            # **エラー発生時のダミープロット**
            print(f"プロットエラー: {e} -> ダミーの図を作成します")
            ax.text(0.5, 0.5, "Error in plot", fontsize=14, ha='center', va='center', color='red')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)
    
        # **ファイル名の決定**
        os.chdir(utils.resultFolder)
        pattern = fName[:-4] + '_*.png'
        file_list = glob.glob(pattern)
    
        if not file_list:
            file_name = f"{fName[:-4]}_{format(printNum, '03')}_0000000.png"
        else:
            max_num = 0
            for file in file_list:
                num = int(os.path.splitext(file)[0].split('_')[-1])
                if num > max_num:
                    max_num = num
            new_num = max_num + 1
            file_name = f"{fName[:-4]}_{format(printNum, '03')}_{new_num:07d}.png"
    
        # **保存**
        fig.savefig(file_name, dpi=200)
        plt.clf()
        plt.close(fig)

    def set_plotList(self, plotList):
        self.plotList = plotList
        
    def set_plotScale(self, plotScale):
        self.plotScale = plotScale
        

class AllPlots:

    def __init__(self):
        self.allPlots = []      # [Plot object_0, Plot object_1, Plot object_2, ---]
        self.plotScale = ""     # This is a temporal parameter, but send to Plot oblect. 
        
    def appendList(self, line_sprit, all_elements):
        l = []  
        for plotElement in line_sprit:            
            if all_elements.get(plotElement) == None:
                pass
            else:
                l.append(all_elements.get(plotElement))
        pl = Plot(Plot_Legend)
        pl.set_plotList(l)
        pl.set_plotScale(self.plotScale)
        self.allPlots.append(pl)
    
    def plotAllElements(self, timeM, step, unit, fName, ShowFigure, utils):
        tRange = [t for t in timeM.csvTimes if t <= step]
        printNum = 1
        # print("Fig_created_by: ", Fig_created_by, ", Fig_from_CSV: ", Fig_from_CSV) 
        # print("allPlots: ", self.allPlots)
        
        try:
            for index, pl in enumerate(self.allPlots, start=1):
                if FIG_OUTPUT == "NO":
                    # Skip plotting and continue the loop if FIG_OUTPUT is "NO"
                    continue
        
                if Fig_created_by == 1 and Optimization == "NO":
                    pl.resultsPlot(tRange, step, unit, fName, printNum, ShowFigure, utils)
                    print("The resultsPlot is pl.resultsPlot.")
                elif Fig_created_by == 2 and Fig_from_CSV == "NO" and Optimization == "NO":
                    pl.resultsPlot_02(timeM, step, unit, fName, printNum, ShowFigure, utils)
                    print("The resultsPlot is pl.resultsPlot_02.")
                elif Fig_created_by == 2 and Fig_from_CSV == "YES" and Optimization == "NO":
                    pl.resultsPlot_03(tRange, step, unit, fName, printNum, ShowFigure, utils)  # 2023.11.3
                    print("The resultsPlot is pl.resultsPlot_03.")
                else:
                    print("")
                    print("******* Error 1 *******" )
                    print('Plotting type Error and/or Optimization == "YES"')
                    # sys.exit()
                    pass
                # printOut for parameter survey  
                if FIG_OUTPUT == "YES" and Optimization == "YES" and step == timeM.endTime:
                    # pl.resultsPlot_04(tRange, step, unit, fName, printNum, ShowFigure, utils, index)  # 2024.4.28
                    pl.resultsPlot_05(tRange, step, unit, fName, printNum, ShowFigure, utils, index)  # 2024.4.28
                    print("The resultsPlot is pl.resultsPlot_05.")
                printNum += 1
        except Exception as e:
            print("\n******* Error 2 *******")
            print("Error in printing process at 'def plotAllElements(---)'")
            print(f"Error type: {type(e).__name__}, Error message: {e}")
            traceback.print_exc()
        
    def plotSetting(self, line_sprit):
        try:
            self.plotScale = line_sprit[1]
        except:
            self.plotScale = "linear"    
        return "*Plot"            


class Utility:
    
    def __init__(self):
        self.plotList = []
        self.resultFolder = ""
        self.plotScale = ""
        self.resultCsv = None
        self.entropyAtCsvTimes = []
        
    def saveDataForPlots(self, step, all_elements):
        for el in all_elements.elements.values():
            el.plotNumbers.append(el.n)
            
    def saveDataForCSV(self, step, all_elements):
        csvData = []
        for el in all_elements.elements.values():
            el.csvNumbers.append(el.n)
            csvData.append(el.n)
            
    def saveCsvFile_001(self, csvTimes, fName, all_elements):               # 2023.12.3
        data = []
        max_int = 1e99  # 設定する整数の上限値
    
        for index, dt in enumerate(csvTimes):
            nl = [el.csvNumbers[index] for el in all_elements.elements.values()]
            # change x to 1e99 if x > max_int
            nl = [x if x <= max_int else max_int for x in nl]
            data.append(nl)

        da2 = np.array(data).T
        da3 = da2.tolist()  
        indxs = [name for name in all_elements.elements.keys()]
        allData = []        
        for id, da in zip(indxs, da3):
            nd = [id]
            nd.extend(da)
            allData.append(nd)     
            
        nCol = ["Name"]
        nCol.extend(csvTimes)
        self.resultCsv = pd.DataFrame(allData, columns = nCol)
        self.resultCsv.to_csv(fName[:-4] + "_all.csv", index=False)                  # 2024.4.13
        
    def saveCsvFile_002(self, csvTimes, fName, all_elements):                       # 2024.4.13       
        data = []
        for index, dt in enumerate(csvTimes):
            nl = [el.csvNumbers[index] for el in all_elements.elements.values()]
            data.append(nl)
            
        indxs = [name for name in all_elements.elements.keys()]  # Get the name of each element
        
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt] + da  # Add pt to the list to extend da
            allData.append(nd)
        
        df = pd.DataFrame(allData, columns=['Time'] + indxs)  # # "Time" in combination with other column names
        df.to_csv(fName[:-4] + "_all_02.csv", index=False)
        
    def saveCsvFile_003(self, fName, all_reactions, timeM):   # 2022.11.19
        data = []
        csvTimes = timeM.getCsvTimes()
        
        # 2025.1.13
        indxs = [name for name in all_reactions.reactions.keys()]
        print("Reaction names in CSV:", [name for name in all_reactions.reactions.keys()])
        
        if EntropyCalc == "YES":
            self._calcEntropy(csvTimes, all_reactions)
        else:
            for r in all_reactions.reactions.values():
                for i, dt in enumerate(csvTimes):
                    r.entropy.append(" - ")
        
        if InformationCalc == "YES":
            for i, dt in enumerate(csvTimes):
                dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
                nl = [r.info[dt_calc] for r in all_reactions.reactions.values()]
                nl += [str(dt_calc)]
                nl += [r.infoAddUp[dt_calc] for r in all_reactions.reactions.values()]
                nl += [str(dt_calc)]
                nl += [r.entropy[i] for r in all_reactions.reactions.values()]
                data.append(nl)
        else:
            for i, dt in enumerate(csvTimes):
                dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
                nl = [" - " for r in all_reactions.reactions.values()]
                nl += [str(dt_calc)]
                nl += [" - " for r in all_reactions.reactions.values()]
                nl += [str(dt_calc)]
                nl += [r.entropy[i] for r in all_reactions.reactions.values()]
                data.append(nl)           
        
        indxs = ["Time\ information"]
        indxs += [k for k in all_reactions.reactions.keys()]
        indxs += ["Time\ infoAddUp"]
        indxs += [k for k in all_reactions.reactions.keys()]
        indxs += ["Time\ entropy"]
        indxs += [k for k in all_reactions.reactions.keys()]
        
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt]
            nd.extend(da)
            allData.append(nd)
            
        df = pd.DataFrame(allData, columns=indxs)
        df.to_csv(fName[:-4] + "_information.csv", index=False)

        
    def saveCsvFile_004(self, fName, all_reactions, timeM):   # 2022.11.19
        data = []
        csvTimes = timeM.getCsvTimes()
        for i, dt in enumerate(csvTimes):
            dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
            nl = [r.n[dt_calc] for r in all_reactions.reactions.values()]
            nl += [str(dt_calc)]
            nl += [r.p_binomial[dt_calc] for r in all_reactions.reactions.values()]
            
            data.append(nl) 
            
        indxs = [r"Time\ number"]
        indxs += [k for k in all_reactions.reactions.keys()]
        indxs += [r"Time\ Probability"]
        indxs += [k for k in all_reactions.reactions.keys()]
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt]
            nd.extend(da)
            allData.append(nd)
        
        df = pd.DataFrame(allData, columns=indxs)
        df.to_csv(fName[:-4] + "_probability.csv", index=False)

    def _calcEntropy(self, csvTimes, all_reactions):
        for r in all_reactions.reactions.values():
            for dt in csvTimes:
                dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
                d = r.forEntropyCalc[dt_calc]          # d[0] is minNK, and d[1] is p
                if d[0] > 1e8:
                    entropy_Shannon = "N/A"
                    print(f"N > 1e8 at {r.reactionName} in def _calcEntropy. ", "entropy_Shannon = 'N/A'")
                    r.entropy.append(entropy_Shannon)
                else:
                    entropy_Shannon = 0
                    try:
                        x = np.arange(0, int(d[0]) + 1, 1)
                        pmf_binom = binom.pmf(x, int(d[0]), d[1])
                    except MemoryError as e:
                        print(f"MemoryError of {r.reactionName} in np.arange()", e)
                    except:
                        print(f"Error at {r.reactionName} in binom.pmf()")
                    try:
                        for p in pmf_binom:
                            try:
                                entropy_Shannon += -p*math.log2(p)
                            except:
                                entropy_Shannon += 0
                    except:
                        entropy_Shannon = "N/A"
                        print(f"Error at {r.reactionName} in def _calcEntropy")
                    r.entropy.append(entropy_Shannon)
                    
                    
    def appendList(self, line_sprit, all_elements):
        el = []  
        for plotElement in line_sprit:            
            if all_elements.get(plotElement) == None:
                pass
            else:
                el.append(all_elements.get(plotElement))            
        self.plotList.append(el)       

    def makeFolder(self, fName):
        dt = datetime.datetime.now()
        y = dt.year; m = dt.month; d = dt.day 
        h = dt.hour; mi = dt.minute; s = dt.second
        if Optimization == "YES":
            dTime = ""
        else:
            dTime = f"_{y}-{m}-{d} {h}-{mi}-{s}"
        fileDir = os.getcwd()
        print('getcwd:      ', fileDir)
        print('__file__:    ', __file__)
        self.resultFolder = fileDir + "/" + fName[:-4] + dTime
        
        if not os.path.exists(self.resultFolder):
            os.makedirs(self.resultFolder)
        
        shutil.copy2(fName, self.resultFolder + "/" + fName)    # 2023.8.5


class TimeManage:
    
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.allTime = []
        self.printTimeInterval = 0
        self.consolPrintTimes = []   # 2022.2.11
        self.plotTimeInterval = 0    # 2022.2.11
        self.plotTimes = []          # 2022.2.11
        self.csvTimeIntercal = 0
        self.csvTimes = []
        self.unit = "-"
        
        self.tRange = []
        self.plot_tRange = []
        self.csv_tRange = []
        
    def setTime(self, line_sprit):
        print("line in *Time: ", line_sprit)
        
        try:
            self.startTime = uf.convert_to_int2(line_sprit[0])
            self.endTime = uf.convert_to_int2(line_sprit[1])
            self.setAllTime()
            pt = int(self.endTime/10)
        except:
            print("*** Error ***")
            print("The *Time discription was wrong.")
            sys.exit()
        
        try:           
            self.setPrintTime(uf.convert_to_int2(line_sprit[2]))
        except:
            self.setPrintTime(pt)
        
        try:
            self.setPlotTimes(uf.convert_to_int2(line_sprit[3]))
        except:
            self.setPlotTimes(pt)
            
        try:
            self.setCsvTimes(uf.convert_to_int2(line_sprit[4]))
        except:
            self.setCsvTimes(pt)
            
        try:
            self.unit = line_sprit[5]
        except:
            self.unit = "-"  
            
        self.calcPlotTimes()
        self.calcPrintTimes()
        self.calcCsvTimes()

    
    def setAllTime(self):  # 2022.8.28
        self.allTime = [t for t in range(self.startTime, self.endTime + 1)]
        
    def setPrintTime(self, ls2):
        self.printTimeInterval = ls2

    def setPlotTimes(self, ls3):
        self.plotTimeInterval = ls3 
        
    def setCsvTimes(self, ls4):
        self.csvTimeInterval = ls4
        
    def calcPlotTimes(self):
        nPlot = (self.endTime - self.startTime)//self.plotTimeInterval
        self.plotTimes = [self.startTime + i*self.plotTimeInterval for i in range(nPlot + 1)]
        print("self.plotTimes = ", self.plotTimes)
        
    def calcPrintTimes(self):
        nPrint = (self.endTime - self.startTime)//self.printTimeInterval
        self.consolPrintTimes = [self.startTime + i*self.printTimeInterval for i in range(nPrint + 1)]     

    def calcCsvTimes(self):
        nPlot = (self.endTime - self.startTime)//self.csvTimeInterval
        self.csvTimes = [self.startTime + i*self.csvTimeInterval for i in range(nPlot + 1)]
        
    def getPrintTimes(self):
        return self.consolPrintTimes
        
    def getPlotTimes(self):
        return self.plotTimes
    
    def getCsvTimes(self):
        return self.csvTimes       

    def getAllTime(self):
        return self.allTime

    def createNewFile(self, fName):
        self.newFileName = fName
        with open(fName, encoding="utf-8_sig") as f:
            setFlg = ""
            setFileName = []
            for line in f:
                if "*End" in line:
                    setFlg = ""
                if setFlg == "Set":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    setFileName.append(line_sprit)
                if "*Set" in line:
                    setFlg = "Set"                 
            self.newFileName = self.makeNewLines(setFileName, fName)
                    
        return self.newFileName
    
    def makeNewLines(self, setFileName, fName):
        if setFileName == []:
            return fName
        else:
            print("setFileName: ", setFileName)
            print("*Set was read. Now under construction!")
            sys.exit()
            return "dummy"
