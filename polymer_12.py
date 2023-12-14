#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:01:58 2021

@author: takashi
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

class Polymer:
    
    def __init__(self):
        self.sumLow_l = []
        self.sumDeg_poly_l = []
        self.sumDeg_geg_poly_l = []
        self.Mw_l = []
        self.Mn_l = []
        self.MwMn_l = []
        self.maxDegrees = 0

    def plotMWD_atAnyTime_02(self, timeM, utils, fName, elms, TimeDataPrint, maxdeg, ShowFigure):
        
        print()
        print("molecular weight distribution of polymers")
        x_max = maxdeg
        self.plotAndPrintForDist(x_max, timeM,
                                 utils, fName, elms, TimeDataPrint, ShowFigure)
            
    def plotAndPrintForDist(self, x_max, timeM, utils, fName, elms, TimeDataPrint, ShowFigure):
        fig = plt.figure()
        xAxis = [ x + 1 for x in range(int(x_max)) ]
        print("xAxis", xAxis)
        plotTime = timeM.getPlotTimes()
        print("plotTime : ", plotTime)
        plt.plot([], [], ' ', label= f"{timeM.unit}")
        for t, d in elms.distributionOfPolymer.items():
            if t in plotTime:
                yAxis = [ d[1][x] for x in range(int(x_max)) ]
                plt.plot( xAxis, yAxis, '.', label=str(t) )
        plt.xlabel("polymer (degrees)",  fontsize=14)
        plt.ylabel("Numbers",  fontsize=14)
        plt.yscale('log')
        plt.legend(loc='best')
        plt.title('Molecular numbers distribution',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        else:
            pass
        if TimeDataPrint == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + "_distribution.png")
        
    def calculateMwMn(self, utils, timeM, fName, elms, TimeDataPrint):
        print()
        rc = utils.resultCsv
        print("rc.columns.values: ", rc.columns.values)
        degrees = self.getDegrees(elms)
        print("degrees: ", degrees)
        start = self.getPolymerItemStart(rc.Name)
        
        for column_name, item in rc.iteritems():
            poly = list(item.iloc[start:])
            if column_name in timeM.getCsvTimes()[1:] :
                row = []
                deg_poly = []
                deg_deg_poly = []
                for n, p in zip(degrees, poly):
                    row.append(p)
                    deg_poly.append(n*p)
                    deg_deg_poly.append(n*n*p)
                sumLow = sum(row)
                sumDeg_poly = sum(deg_poly)
                sumDeg_geg_poly = sum(deg_deg_poly)
                Mw = sumDeg_geg_poly/sumDeg_poly
                Mn = sumDeg_poly/sumLow
                MwMn = Mw/Mn                 
                print(f" Mw : {Mw}")
                print(f" Mn : {Mn}")
                print(f" Mw/Mn : {MwMn}")
                self.sumLow_l.append(sumLow)
                self.sumDeg_poly_l.append(sumDeg_poly)
                self.sumDeg_geg_poly_l.append(sumDeg_geg_poly)
                self.Mw_l.append(Mw)
                self.Mn_l.append(Mn)
                self.MwMn_l.append(MwMn)

    def getDegrees(self, elms):
        degrees = []
        for el in elms.polymers.values():
            if el.type == "M=*_R":
                degrees.append(el.degrees)
            elif el.type == "M=*":
                degrees.append(el.degrees)  
        return degrees
    
    def getPolymerItemStart(self, name):
        start = 0
        for index, it in enumerate(list(name)):
            if "M=" in it:
                start = index
                break
        return start
        
    def plotDistribution(self, time, utils, fName, elms, TimeDataPrint, ShowFigure):
        fig = plt.figure()
        graph_x = []
        graph_y = []
        graph_x_r = []
        graph_y_r = []
        graph_x_p = []
        graph_y_p = []
        for el in elms.polymers.values():
            if el.type == "M=*_R":
                graph_x_r.append(el.degrees)
                graph_y_r.append(el.n)  
            elif el.type == "M=*":
                graph_x_p.append(el.degrees)
                graph_y_p.append(el.n)                  
            graph_x.append(el.degrees)
            graph_y.append(el.n)   
        plt.plot(graph_x_r, graph_y_r, label="M=*_R")
        plt.plot(graph_x_p, graph_y_p, label="M=*")            
        elms.distributionOfPolymer[time] = (graph_x, graph_y)       
        plt.xlabel("polymer (degrees)",  fontsize=14)
        plt.ylabel("Numbers",  fontsize=14)
        plt.yscale('log')
        plt.legend(loc='best')
        plt.title(f'Molecular numbers distribution @time = {time}',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        else:
            pass
        if TimeDataPrint == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + f"_t={format(time, '06')}.png")
            
    def saveDistribution(self, utils, timeM, fName):
        data = [[0, 0, 0, 0]]
        for t, mw, mn, mwmn in zip(timeM.getPlotTimes()[1:], self.Mw_l, self.Mn_l, self.MwMn_l):
            md = [t, mw, mn, mwmn]
            data.append(md)
        indxs = ["Time", "Mw", "Mn", "Mw/Mn"]
        df_03 = pd.DataFrame(data, columns=indxs, index = timeM.getPlotTimes())
        df_03.to_csv(fName[:-4] + "_MwMn.csv")
    
    def plotMwMn(self, utils, timeM, fName, ShowFigure):
        fig = plt.figure()
        xAxis = timeM.getCsvTimes()[1:]
        plt.plot(xAxis, self.Mw_l, marker='+', label= "Mw")
        plt.plot(xAxis, self.Mn_l, marker='+', label= "Mn")
        plt.xlabel(f"time ({timeM.unit})",  fontsize=14)
        plt.ylabel("Mw and Mn",  fontsize=14)
        plt.yscale('log')
        plt.legend(loc='best')
        plt.title('Molecular weight',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        else:
            pass
        os.chdir(utils.resultFolder)
        fig.savefig(fName[:-4] + "_MwMn.png")          
        
        fig = plt.figure()
        # xAxis = timeM.getPlotTimes()
        plt.plot(xAxis, self.MwMn_l, marker='o', color='r', label= "Mw/Mn")
        plt.xlabel(f"time ({timeM.unit})",  fontsize=14)
        plt.ylabel("Mw/Mn",  fontsize=14)
        plt.legend(loc='best')
        plt.title('Molecular weight polydispersibility',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        else:
            pass
        os.chdir(utils.resultFolder)
        fig.savefig(fName[:-4] + "_MwMn_02.png")
        
    def getMaxDegrees(self, polymers):
        maxdeg = 0
        for k, p in polymers.items():
            if p.degrees > maxdeg:
                maxdeg = p.degrees
        self.maxDegrees = maxdeg
        print("maxdeg = ", maxdeg)
        return maxdeg
            




