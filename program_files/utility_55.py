#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:05:35 2020

@author: takashi
"""

import sys, os
import numpy as np
import shutil
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import json
import math
from scipy.stats import binom


global config, EntropyCalc, CSV_OUTPUT, FIG_OUTPUT, RestartFile


def _load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def init(filename):
    global config, EntropyCalc, CSV_OUTPUT, FIG_OUTPUT, RestartFile
    config = _load_config(filename)
    EntropyCalc = config["settings"]["EntropyCalc"]
    CSV_OUTPUT = config["settings"]["CSV_OUTPUT"]
    FIG_OUTPUT = config["settings"]["FIG_OUTPUT"]
    RestartFile = config["settings"]["RestartFile"]


class Plot:
    
    def __init__(self):
        self.plotList = []
        self.plotScale = ""
    
    def resultsPlot(self, tRange, time, unit, fName, printNum, ShowFigure, utils):   
        fig = plt.figure()       
        for elem in self.plotList :
            plt.plot(tRange, elem.currentNums, 
                     marker=elem.marker, markersize=4, 
                     label=elem.name, color=elem.color)
        plt.xlabel(f"time ({unit})", fontsize=14)
        plt.ylabel("Number", fontsize=14)
        plt.yscale(self.plotScale)
        plt.legend(loc='best')
        title = 'Number of the element'
        plt.title(title, loc='center',fontsize=14)
           
        if ShowFigure == "YES" and time != 0:  # 2023.3.25
            plt.show()     
        else:
            pass
        if FIG_OUTPUT == "YES":
            os.chdir(utils.resultFolder)            
            fig.savefig(fName[:-4] + f"_t={format(time, '06')}_{format(printNum, '03')}.png", dpi=200)
        plt.clf()
        plt.close()        
              
    def set_plotList(self, plotList):
        self.plotList = plotList
        
    def set_plotScale(self, plotScale):
        self.plotScale = plotScale
        

class AllPlots:

    def __init__(self):
        self.allPlots = []
        self.plotScale = ""
        
    def appendList(self, line_sprit, all_elements):
        l = []  
        for plotElement in line_sprit:            
            if all_elements.get(plotElement) == None:
                pass
            else:
                l.append(all_elements.get(plotElement))
        pl = Plot()
        pl.set_plotList(l)
        pl.set_plotScale(self.plotScale)
        self.allPlots.append(pl)
    
    def plotAllElements(self, tRange, time, unit, fName, ShowFigure, utils):
        printNum = 1
        for pl in self.allPlots:
            pl.resultsPlot(tRange, time, unit, fName, printNum, ShowFigure, utils)
            printNum += 1
        
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

    def saveCsvFile(self, time, csvTimes, fName, all_elements, timeM):
        data = []
        print("csvTimes: ", csvTimes)
        for dt in csvTimes:
            dt_calc = dt - csvTimes[0]
            nl = [v.currentNums[dt_calc] for v in all_elements.elements.values()]
            data.append(nl)
        da2 = np.array(data).T
        da3 = da2.tolist()  
        indxs = [k for k, v in all_elements.elements.items()]
        
        allData = []        
        for id, da in zip(indxs, da3):
            nd = [id]
            nd.extend(da)
            allData.append(nd)        
        nCol = ["Name"]
        nCol.extend(csvTimes)
        self.resultCsv = pd.DataFrame(allData, columns = nCol)
        self.resultCsv.to_csv(fName[:-4] + "_all.csv")

    def saveCsvFile_02(self, time, csvTimes, fName, all_elements, timeM):
        data = []
        for dt in csvTimes:  
            dt_calc = dt - csvTimes[0]                                           # 2022.12.21
            nl = [v.currentNums[dt_calc] for v in all_elements.elements.values()]
            data.append(nl)        
        indxs = [k for k, v in all_elements.elements.items()]
        indxs.insert(0, "Time")
        
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt]
            nd.extend(da)
            allData.append(nd)        
        df = pd.DataFrame(allData, columns=indxs, index = csvTimes)
        df.to_csv(fName[:-4] + "_all_02.csv")
        
    def saveCsvFile_03(self, time, csvTimes, fName, all_reactions, timeM):   # 2022.11.19
        data = []
        print("csvTimes: ", csvTimes)
        if EntropyCalc == "YES":
            self._calcEntropy(csvTimes, all_reactions, timeM)
        else:
            for r in all_reactions.reactions.values():
                for i, dt in enumerate(csvTimes):
                    r.entropy.append("  - ")
        
        for i, dt in enumerate(csvTimes):
            dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
            nl = [r.info[dt_calc] for r in all_reactions.reactions.values()]
            nl += [str(dt_calc)]
            nl += [r.infoAddUp[dt_calc] for r in all_reactions.reactions.values()]
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
            
        df = pd.DataFrame(allData, columns=indxs, index = csvTimes)
        df.to_csv(fName[:-4] + "_information.csv")

    def _calcEntropy(self, csvTimes, all_reactions, timeM):
        for r in all_reactions.reactions.values():
            for dt in csvTimes:
                dt_calc = dt - csvTimes[0]                                  # 2023.9.10  
                d = r.forEntropyCalc[dt_calc]    # d[0] is minNK, and d[1] is p
                # print(f"N = {int(d[0])}, p = {d[1]} in {r.reactionName}")
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
        dTime = f"_{y}-{m}-{d} {h}-{mi}-{s}"
        fileDir = os.getcwd()
        print('getcwd:      ', fileDir)
        print('__file__:    ', __file__)
        self.resultFolder = fileDir + "/" + fName[:-4] + dTime
        os.mkdir(self.resultFolder)
        shutil.copy2(fName, self.resultFolder + "/" + fName)    # 2023.8.5


class TimeManage:
    
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.allTime = []
        self.printTimeInterval = 0
        self.printTimes = []   # 2022.2.11
        self.plotTimeInterval = 0   # 2022.2.11
        self.plotTimes = []   # 2022.2.11
        self.csvTimeIntercal = 0
        self.csvTimes = []
        self.unit = "-"
        self.csvTimes_in_calc = []
        
    def setTime(self, line_sprit):
        for term in range(5):
            if type(int(line_sprit[term])) == int:
                pass
            else:
                print(" ")
                print("*** Error ***")
                print("The *Time discription was wrong.")
                print("You needs five int characters.")
                print("*** Error ***")
                print(" ")
                sys.exit()                
             
        try:
            self.startTime = int(line_sprit[0])
            self.endTime = int(line_sprit[1])
            self.setAllTime()
            pt = int(self.endTime/10)
        except:
            print("*** Error ***")
            print("The *Time discription was wrong.")
            sys.exit()
        
        try:           
            self.setPrintTime(int(line_sprit[2]))
        except:
            self.setPrintTime(pt)
        
        try:
            self.setPlotTimes(int(line_sprit[3]))
        except:
            self.setPlotTimes(pt)
            
        try:
            self.setCsvTimes(int(line_sprit[4]))
        except:
            self.setCsvTimes(pt)
            
        try:
            self.unit = line_sprit[5]
        except:
            self.unit = "-"  
            
        self.calcPlotTimes()
        self.calcPrintTimes()
        self.calcCsvTimes()
        self.calcCalculationTime()
    
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
        self.printTimes = [self.startTime + i*self.printTimeInterval for i in range(nPrint + 1)]
        print("self.printTimes = ", self.printTimes)        

    def calcCsvTimes(self):
        nPlot = (self.endTime - self.startTime)//self.csvTimeInterval
        self.csvTimes = [self.startTime + i*self.csvTimeInterval for i in range(nPlot + 1)]
        print("self.csvTimes = ", self.csvTimes)
        
    def calcCalculationTime(self):
        self.csvTimes_in_calc = list(np.array(self.csvTimes) - self.startTime)
        print("self.csvTimes_in_calc: ", self.csvTimes_in_calc)

    def getPrintTimes(self):
        return self.printTimes
        
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
