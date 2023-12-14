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
import glob
import platform

def setFromTerminal(fName, ShowInSpyder):
    try:
        fName = sys.argv[1]
        print(f"A input file {fName} is read from terminal.")
        ShowInSpyder = "NO"
    except:
        pass

    print("ShowInSpyder = " , ShowInSpyder)

    try:
        print(fName)
        print(f"A input file {fName} is read from Spyder.")
    except:
        print("You need one input file.")
        sys.exit()
        
    return fName, ShowInSpyder


def changeDirectory(fName):
    dName = ""
    thisOS = platform.system()
    for name in glob.glob("./*/*"):
        # 2022.3.3
        if thisOS == "Windows":        
            name = name.split("\\")       # Windows
        else:
            name = name.split("/")      # Linux
        # 2022.3.3    
        if name[-1] == fName:
            dName = name[-2]     
    print(f"The directory name is {dName}.")
    os.chdir(dName)    


class Utility:
    
    def __init__(self):
        self.plotList = []
        self.resultFolder = ""
        self.plotScale = ""
        self.resultCsv = None
        
    def plotSome(self, tRange, time, unit, fName, TimeDataPrint, ShowInSpyder):  
        printNum = 1
        for PList in self.plotList:
            self.resultsPlot(tRange, PList, time, unit, fName, TimeDataPrint, printNum, ShowInSpyder)
            printNum += 1
    
    def resultsPlot(self, tRange, PList, time, unit, fName, TimeDataPrint, printNum, ShowInSpyder):   
        fig = plt.figure()         
        for elem in PList :
            plt.plot(tRange, elem.currentNums, 
                     marker=elem.marker, markersize=4, 
                     label=elem.name, color=elem.color)
        plt.xlabel(f"time ({unit})", fontsize=14)
        plt.ylabel("Number", fontsize=14)
        plt.yscale(self.plotScale)
        plt.legend(loc='best')
        title = 'Number of the element'
        plt.title(title, loc='center',fontsize=14)
        if ShowInSpyder == "YES" and time != 0:  # 2022.12.17     
            plt.show()     
        else:
            pass
        if TimeDataPrint == "YES": 
            os.chdir(self.resultFolder)            
            fig.savefig(fName[:-4] + f"_t={format(time, '06')}_{format(printNum, '03')}.png")

    def saveCsvFile(self, time, csvTimes, fName, elms, timeM):
        data = []
        for dt in csvTimes:
            nl = [v.currentNums[dt] for v in elms.allElements.values()]
            data.append(nl)
        da2 = np.array(data).T
        da3 = da2.tolist()  
        indxs = [k for k, v in elms.allElements.items()]
        
        allData = []        
        for id, da in zip(indxs, da3):
            nd = [id]
            nd.extend(da)
            allData.append(nd)        
        nCol = ["Name"]
        nCol.extend(csvTimes)
        self.resultCsv = pd.DataFrame(allData, columns = nCol)
        self.resultCsv.to_csv(fName[:-4] + "_all.csv")

    def saveCsvFile_02(self, time, csvTimes, fName, elms, timeM):
        data = []
        for dt in csvTimes:                                             # 2022.12.21
            nl = [v.currentNums[dt] for v in elms.allElements.values()]
            data.append(nl)        
        indxs = [k for k, v in elms.allElements.items()]
        indxs.insert(0, "Time")
        
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt]
            nd.extend(da)
            allData.append(nd)        
        df = pd.DataFrame(allData, columns=indxs, index = csvTimes)
        df.to_csv(fName[:-4] + "_all_02.csv")
        
    def saveCsvFile_03(self, time, csvTimes, fName, reacs, timeM):   # 2022.11.19
        data = []
        print("csvTimes: ", csvTimes)
        for dt in csvTimes:
            nl = [v.info[dt] for v in reacs.allReactions.values()]
            nl += [str(dt)]
            nl += [v.infoAddUp[dt] for v in reacs.allReactions.values()]
            data.append(nl)
        
        indxs = ["Time"]
        indxs += [k for k, v in reacs.allReactions.items()]
        indxs += ["Time"]
        indxs += [k for k, v in reacs.allReactions.items()]
        
        allData = []   
        for pt, da in zip(csvTimes, data):
            nd = [pt]
            nd.extend(da)
            allData.append(nd)
            
        df = pd.DataFrame(allData, columns=indxs, index = csvTimes)
        df.to_csv(fName[:-4] + "_all_03.csv")


    def appendList(self, line_sprit, allElements):
        l = []  
        for plotElement in line_sprit:            
            if allElements.get(plotElement) == None:
                pass
            else:
                l.append(allElements.get(plotElement))            
        self.plotList.append(l)       

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
        shutil.copy2(fName, self.resultFolder + "/" + fName)
        
    def makeUnits(self, line_sprit, elms, reacs):
        print(line_sprit)
        if line_sprit[0] == "element":
            pass


class timeManage:
    
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.allTime = []
        self.printTimeInterval = 0
        self.printTimes = []   # 2022.2.11
        self.plotTimeInterval = 0   # 2022.2.11
        self.plotTimes = []   # 2022.2.11
        self.csvTimeIntercal = 0
        self.cavTimes = []
        self.unit = "-"
        
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
            print(setFileName)
            print("*Set was read. Now under construction!")
            sys.exit()
            return "dummy"
