#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:05:35 2020

@author: Takashi Sato
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
        
    def appendList(self, ls, el):
        l = []       
        for em in ls:
            l.append(el[em.split()[0]])   
            
        self.plotList.append(l)
#        print(self.plotList)