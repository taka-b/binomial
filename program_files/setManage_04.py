#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:32:14 2023

@author: takashi
"""

import sys

class Set:
    
    def __init__(self, setName, allElements, allReactions, allPlots):
        self.setName = setName
        self.elements = {}
        self.reactions = {}
        self.plots = []
        
    def add_element(self, elemName, allElements):
        newElementName = elemName
        if elemName in self.elements.keys():
            print(f"Element {elemName} already exists")
            sys.exit() 
        elif "_inter" in self.setName:
            newElementName = self.rename_element(elemName, self.setName, allElements)

        self.elements[newElementName] = allElements.elements[newElementName]
        print(f"A element: {newElementName} is added in Set: {self.setName}")
            
    def add_reaction(self, reacName, allReactions):
        newReactionName = reacName
        if reacName in self.reactions.keys():
            print(f"Reaction {reacName} already exists")
            sys.exit()     
        elif  "_inter" in self.setName:
            newReactionName = self.rename_reaction(reacName, self.setName, allReactions)
            
        self.reactions[newReactionName] = allReactions.reactions[newReactionName]
        print(f"A reaction: {newReactionName} is added in Set: {self.setName}")

    def add_plot(self, plotName, allPlots):
        newPlotName = plotName
        
        # Plot is safe for dupulicate!      2025.1.16
        
        # if plotName in self.plots:
        #     print(f"Plots {plotName} already exists")
        #     sys.exit()     
        # elif "_inter" in self.setName:
        #     newPlotName = self.rename_plot(plotName, self.setName, allPlots)
            
        self.plots.append(newPlotName)
        print(f"Plots: {newPlotName} is added in Set: {self.setName}")
            
    def rename_element(self, elemName, setName, allElements):
        # 
        if elemName not in allElements.elements:
            print(f"Error: Element {elemName} does not exist.")
            sys.exit()
        el = allElements.elements.pop(elemName)
        new_name = elemName + setName
        
        # check_duplicate
        if new_name in allElements.elements:
            print(f"Error: Element {new_name} already exists in allElements. Cannot rename {elemName}.")
            sys.exit()
        
        el.rename(new_name)
        allElements.elements[el.name] = el
        
        # check_duplicate in allSets
        # for s in allSets.values():
        #     if elemName in s.elements:
        #         s.elements[new_name] = s.elements.pop(elemName)
        #         print("check_duplicate in allSets")
        
        return el.name 
    
    def rename_reaction(self, reacName, setName, allReactions):
        re = allReactions.reactions.pop(reacName)
        new_reacName = reacName + setName
        re.rename(new_reacName)
        allReactions.reactions[re.reactionName] = re
        return re.reactionName
    
    # def rename_plot(self, plotName, setName, allPlots):
    #     newPlotList = []
    #     plot = allPlots.allPlots.pop(plotName)
    #     print(f"Plot List : {plot.plotList}")
    #     for pNames in plot.plotList:
    #         newPlotList.append(pName + setName)
    #     return newPlotName


class allSets:
    
    def __init__(self):
        
        self.allSets = {}
        
    def createSet(self, setName, allElements, allReactions, allPlots):
        if setName in self.allSets.keys():
            pass
        else:
            self.allSets[setName] = Set(setName, allElements, allReactions, allPlots)
            
        print(f"\n !!! A set: {setName} is created. !!! \n")
        
    def addSetElements(self, setName, elemName, allElements):
        self.allSets[setName].add_element(elemName, allElements)
        # print(f"  {self.allSets.keys()}")
        
    def addSetReactions(self, setName, reacName, allReactions):
        self.allSets[setName].add_reaction(reacName, allReactions)
        
    def addSetPlots(self, setName, plotName, allPlots):
        self.allSets[setName].add_plot(plotName, allPlots)
        
        