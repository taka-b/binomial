#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:32:14 2023

@author: takashi
"""

class Set:
    
    def __init__(self, setName):
        self.setName = setName
        self.elements = {}
        self.reactions = {}
        self.plots = {}
        
    def add_element(self, eName, element):
        if eName in self.elements.keys():
            print(f"Element {eName} already exists")
        else:
            self.elements[eName] = element
            
    def add_reaction(self, rName, reaction):
        if rName in self.reactions.keys():
            print(f"Reaction {rName} already exists")
        else:
            self.reactions[rName] = reaction 

    def add_plot(self, plots, all_plot):
        for p in plots:
            if p in self.plots.keys():
                print(f"Plot {p} already exists")
            else:
                self.plots[p]    
        

class allSets:
    
    def __init__(self):
        
        self.allSets = {}
        
    def createSet(self, setName):
        if setName in self.allSets.keys():
            pass
        else:
            self.allSets[setName] = Set(setName)     
        
    def addSetElements(self, setName, elemName, all_elem):
        self.allSets[setName].add_element(elemName, all_elem.allElements[elemName])
        