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
            
    def plotAndPrintForDist(self, timeM, utils, fName, elms, FIG_OUTPUT, x_max, ShowFigure):
        fig = plt.figure()
        xAxis = [ x + 1 for x in range(int(x_max)) ]
        plotTime = timeM.getPlotTimes()
        print("plotTime : ", plotTime)
        plt.plot([], [], ' ', label= f"{timeM.unit}")
        for t, d in elms.distributionOfPolymer.items():
            if t in plotTime:
                yAxis = [ d[1][x] for x in range(int(x_max)) ]
                plt.plot( xAxis, yAxis, label=str(t) )
        plt.xlabel("polymer (degrees)",  fontsize=14)
        plt.ylabel("Numbers",  fontsize=14)
        plt.legend(loc='best')
        plt.yscale('log')
        plt.title('Molecular numbers distribution (log)',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        if FIG_OUTPUT == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + f"_distribution_log.png")
        
        fig = plt.figure()
        plt.plot([], [], ' ', label= f"{timeM.unit}")
        for t, d in elms.distributionOfPolymer.items():
            if t in plotTime:
                yAxis = [ d[1][x] for x in range(int(x_max)) ]
                plt.plot( xAxis, yAxis, label=str(t) )
        plt.xlabel("polymer (degrees)",  fontsize=14)
        plt.ylabel("Numbers",  fontsize=14)
        plt.legend(loc='best')        
        plt.yscale('linear')
        plt.title('Molecular numbers distribution (linear) ',loc='center', fontsize=14)
        if ShowFigure == "YES":  # 2022.6.26
            plt.show()     
        if FIG_OUTPUT == "YES":
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + "_distribution_linear.png")
        
    def calculateMwMn(self, utils, timeM, fName, elms, TimeDataPrint):
        print()
        rc = utils.resultCsv
        print("rc.columns.values: ", rc.columns.values)
        degrees = self._getDegrees(elms)
        # print("degrees: ", degrees)
        start = self._getPolymerItemStart(rc.Name)
        
        for column_name, item in rc.iteritems():
            poly_Num = list(item.iloc[start:])
            if column_name in timeM.getCsvTimes()[1:] :
                row = []
                deg_poly = []
                deg_deg_poly = []
                for n, p_Num in zip(degrees, poly_Num):
                    row.append(p_Num)
                    deg_poly.append(n*p_Num)
                    deg_deg_poly.append(n*n*p_Num)
                sumLow = sum(row)
                sumDeg_poly = sum(deg_poly)
                sumDeg_geg_poly = sum(deg_deg_poly)
                Mw = sumDeg_geg_poly/sumDeg_poly
                Mn = sumDeg_poly/sumLow
                MwMn = Mw/Mn                 
                self.sumLow_l.append(sumLow)
                self.sumDeg_poly_l.append(sumDeg_poly)
                self.sumDeg_geg_poly_l.append(sumDeg_geg_poly)
                self.Mw_l.append(Mw)
                self.Mn_l.append(Mn)
                self.MwMn_l.append(MwMn)

    def _getDegrees(self, elms):
        degrees = []
        for el in elms.polymers.values():
            if el.type == "M=*_R":
                degrees.append(el.degrees)
            elif el.type == "M=*":
                degrees.append(el.degrees)  
        return degrees
    
    def _getPolymerItemStart(self, name):
        start = 0
        for index, it in enumerate(list(name)):
            if "M=" in it:
                start = index
                break
        return start
            
    def plotDistribution(self, time, utils, fName, elms, FIG_OUTPUT, ShowFigure):
        g_x_r = []
        g_y_r = []
        g_x_p = []
        g_y_p = []
        for el in elms.polymers.values():
            if el.type == "M=*_R":
                g_x_r.append(el.degrees)
                g_y_r.append(el.n)  
            elif el.type == "M=*":
                g_x_p.append(el.degrees)
                g_y_p.append(el.n)
        g_x = [a + b for a, b in zip(g_x_r, g_x_p)] + g_x_r[len(g_x_p):] + g_x_p[len(g_x_r):]    
        g_y = [a + b for a, b in zip(g_y_r, g_y_p)] + g_y_r[len(g_y_p):] + g_y_p[len(g_y_r):] 
        elms.distributionOfPolymer[time] = (g_x, g_y)      
        # Linear scale plot
        fig = plt.figure()
        plt.plot(g_x_r, g_y_r, label="M=*_R")
        plt.plot(g_x_p, g_y_p, label="M=*")
        plt.xlabel("polymer (degrees)", fontsize=14)
        plt.ylabel("Numbers", fontsize=14)
        plt.yscale('linear')
        plt.legend(loc='best')
        plt.title(f'Molecular numbers distribution (linear) @time = {time}', fontsize=14)
        if ShowFigure == "YES":
            plt.show()
        if FIG_OUTPUT == "YES":    
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + "_MND (linear)" + f"_t={format(time, '06')}.png")
        # Log scale plot
        fig = plt.figure()
        plt.plot(g_x_r, g_y_r, label="M=*_R")
        plt.plot(g_x_p, g_y_p, label="M=*")
        plt.xlabel("polymer (degrees)", fontsize=14)
        plt.ylabel("Numbers", fontsize=14)
        plt.yscale('log')
        plt.legend(loc='best')
        plt.title(f'Molecular numbers distribution (log) @time = {time}', fontsize=14)
        if ShowFigure == "YES":
            plt.show()
        if FIG_OUTPUT == "YES":     
            os.chdir(utils.resultFolder)
            fig.savefig(fName[:-4] + "_MND (log)" + f"_t={format(time, '06')}.png")
            
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
            




