#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:05:35 2020

@author: takashi
"""

import matplotlib.pyplot as plt


class Utility:
    
    def __init__(self):
        self.plotList = []
        
    def plotAll(self, time):       
        for pl in self.plotList:
         self.resultsPlot(time, pl)
    
    def resultsPlot(self, time, PList):            
        for elem in PList :
            plt.plot(time, elem.currentNums, '.', label=elem.name, color = elem.color )
        plt.xlabel("time",  fontsize=24)
        plt.ylabel("Numbers",  fontsize=24)
        plt.legend(loc='best')
        plt.show()
        
    def appendList(self, line_sprit, allElements):
        l = []       
        for plotElement in line_sprit:            
            if allElements.get(plotElement) == None:
                pass
            else:
                l.append(allElements.get(plotElement))            
        self.plotList.append(l)

