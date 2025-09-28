#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 18:00:04 2022

@author: takashi
"""

import os
import itertools

allnewNameDict = {}
# newNameDict_01 = {}
newNameDict_02 = {}

def createNewFile(fName):
    ''' 
    create a new input file, if the fName-file has *Set  

    Parameters
    ----------
    fName : strings
        an original main input-file name with ".txt"

    Returns
    -------
        a new input-file name with ".txt"

    '''
    newFileName = fName
    f_main = open(fName, 'r', encoding='UTF-8_sig')
    data_main = f_main.readlines() 
    
    with open(fName, encoding="utf-8_sig") as f:
        setFlg = ""
        setLines_01 = []
        setLines_02 = []
        setLines_01_inter = []
        delete_flag = False
        setFlg = ""
        for line in f:
            line_new = line.replace('\n','')
            line_parts = [x.strip() for x in line_new.split(",")]
            if line_parts[0] == '' or '**' in line_parts[0] or '#' in line_parts[0]:
                pass        
            elif "*Plot" in line or "*End" in line:
                setFlg = ""      
                delete_flag = False
            elif "*Set_01" in line:
                setFlg = "*Set_01"
                delete_flag = True
            elif "*Set_02" in line:
                setFlg = "*Set_02"
                delete_flag = True
            # 2025.1.9
            elif  "*Set01_inter" in line:
                setFlg = "*Set01_inter"
                
            # action    
            elif setFlg == "*Set_01":
                line_new = line.replace('\n','')
                line_parts = [x.strip() for x in line_new.split(",")]
                setLines_01.append(line_parts)
                delete_flag = True
            elif setFlg == "*Set_02":
                line_new = line.replace('\n','')
                line_parts = [x.strip() for x in line_new.split(",")]
                setLines_02.append(line_parts)
                delete_flag = True
            # 2025.1.9    
            elif setFlg == "*Set01_inter":
                line_new = line.replace('\n','')
                line_parts = [x.strip() for x in line_new.split(",")]
                setLines_01_inter.append(line_parts)
                delete_flag = True            
                
                print("setLines_01_inter: \n" , setLines_01_inter)
                
            else:
                delete_flag = False
                
            if delete_flag:
                _prependAsterisk(data_main, line)
                
            
                    
    newFileName = _makeNewFileName(fName, setLines_01)
    newLines_01 = _make_Set_01(data_main, setLines_01)                                    # 2025.1.9
    newLines_02 = _make_Set_02(setLines_02)
    newLines_01.extend(newLines_02)
    
    # 2025.1.9
    newLines_03 = _make_Set01_inter(setLines_01_inter)
    newLines_01.extend(newLines_03)                                                       # 2025.1.9
    
    _writeNewFile(newLines_01, newFileName)      # temp 2022.12.11
    return newFileName
    
def _prependAsterisk(data_main, line):
    index = data_main.index(line)
    data_main[index] = "** " + line
    
def _makeNewFileName(fName, setLines_01):
    if setLines_01 == []:
        newFileName = fName
    else:
        newFileName = fName[:-4] + "_new" + ".txt" 
    print("\n newFileName at *Set_01 is : ", newFileName)
    return newFileName

def _make_Set_01(data_main, setLines_01):
    newLines_01 = []
    newLines_01.append(data_main)
    # newNameDict_01 = {}
    print("setLines_01: \n", setLines_01)
    for set_line in setLines_01:
        newLines, newNames = _write_Set_01(set_line)
        newLines_01.append(newLines)
    newLines_01 = list(itertools.chain.from_iterable(newLines_01)) 
    return newLines_01

def _write_Set_01(set_line):
    newNames = []
    newLines = []
    print("set_line: \n", set_line)
    for n in range(int(set_line[2])):
        newNames.append(set_line[0] + "_" + str(n + 1))
    print("newNames: \n", newNames)
    
    f = open(set_line[1], 'r', encoding='UTF-8_sig')
    setFile = f.readlines()
    f.close()    
    for nName in newNames:
        newData = _create_Set_01(setFile, nName)
        newLines.append(newData)
    newLines = list(itertools.chain.from_iterable(newLines))    
    return newLines, newNames

def _create_Set_01(setFile, nName):
    # 2023.2.19
    newData = [" \n",
               " \n",
               "** ************************************ \n",
               "*SetDefine, " + ":="+nName + "\n",                # 2025.1.8   
               "** ************************************ \n"]      # under constraction
    for line in setFile:
        ls = line.split(",")
        newls = []
        for s in ls:
            if "\n" in s: 
                t = s
            else:
                t = s + ", "
            if ":=" in s:
                v = s.split(":=")
                t = v[0] + ":=" + nName
                if "\n" in s:
                    t = t + "\n"
                else:
                    t = t + ", "                    
            newls.append(t)
        newData.append(newls)
    newData = list(itertools.chain.from_iterable(newData))
    return newData    

def _make_Set_02(setLines_02):
    newLines_02 = []
    print("setLines_02: \n", setLines_02) 
    for setLine in setLines_02:
        newLines, newNames = _write_Set_02(setLine)
        newLines_02.append(newLines)
    newLines_02 = list(itertools.chain.from_iterable(newLines_02))  
    return newLines_02

def _write_Set_02(sL):
    print("setLine: \n", sL) 
    # newSet = {}
    newNames = []
    newLines = []
    setName = sL[0]
    setFirstName = sL[1]
    setFirstNum = int(sL[2])
    SecondfileName = sL[3]
    setSecondNum = int(sL[4])
    for sFn in range(setFirstNum):
       for sSn in range(setSecondNum): 
           newName = setFirstName + "_" + str(sFn+1) + "::" + setName + "_" + str(sSn+1) 
           newNames.append(newName)
           print("new_Name of *Set_02: ", newName)
    
    f = open(SecondfileName, 'r', encoding='UTF-8_sig')
    setFile = f.readlines()
    f.close()  
    
    for nName in newNames:
        newData = _create_Set_02(setFile, nName)
        newLines.append(newData)
    newLines = list(itertools.chain.from_iterable(newLines))    
    return newLines, newNames

def _create_Set_02(setFile, nName):
    # 2023.4.29
    newData = [" \n",
               " \n",
               "** ************************************ \n",
                "*SetDefine, " + "::" + nName + "\n",              # 2025.1.8    
                "** ************************************ \n"]      # under constraction
                                                                   # Why does this have "if ":=" in s:" ?
    nName_first = nName.split("::")[0]
    for line in setFile:
        ls = line.split(",")
        newls = []
        for s in ls:
            if "\n" in s: 
                t = s
            else:
                t = s + ", "
            if ":=" in s:
                v = s.split(":=")
                t = v[0] + ":=" + nName_first
                if "\n" in s:
                    t = t + "\n"
                else:
                    t = t + ", "    
            elif "::" in s:
                v = s.split("::")
                t = v[0] + "::" + nName
                if "\n" in s:
                    t = t + "\n"
                else:
                    t = t + ", "
            newls.append(t)
        newData.append(newls)
    newData = list(itertools.chain.from_iterable(newData))
    return newData    

# 2025.1.9
def _make_Set01_inter(setLines_01_inter):
    newLines_03 = []
    for setLine in setLines_01_inter:
        newLines, newNames = _write_Set01_inter(setLine)
        newLines_03.append(newLines)
    newLines_03 = list(itertools.chain.from_iterable(newLines_03))  
    return newLines_03

def _write_Set01_inter(sL):
    print("setLine: \n", sL) 
    newNames = []        # This is not used.

    setName = sL[0]
    setFileName = sL[1]
    newLines = [" \n",
               " \n",
               "** ************************************ \n",
                "*SetDefine, " + ":=:" + setName + "\n",              # 2025.1.8    
                "** ************************************ \n"]
    
    f = open(setFileName, 'r', encoding='UTF-8_sig')
    setFile = f.readlines()
    f.close()  
    
    for sl in setFile:
        newLines.append(sl)
    newLines.append(["\n\n"])
    newLines = list(itertools.chain.from_iterable(newLines))    
    return newLines, newNames


def _writeNewFile(newLines, newFileName):
    print("def _writeNewFile: ")
    with open(newFileName, 'w') as f:
        f.writelines(newLines)


def openReadFile(fName, allElements, allReactions, timeM, utils, poly, allPlots, allSets):

    InputItems = {"*Time": timeM.setTime, 
                  "*Element": allElements.setElement,
                  "*ElementInOut": allElements.setElementInOut,
                  "*elementPolymer": allElements.setElementPolymer,
                  "*Comment": commentLine
                  }
    with open(fName, encoding="utf-8_sig") as f:   # windows needs encoding="utf-8_sig"
        current_flag = 0
        subFlg = 0#!/
        normConst = 0
        Lines_for_rM = []     
        print("f in openReadFile: ", fName)
        
        for line in f:
            line_new = line.replace('\n','')
            line_parts = [x.strip() for x in line_new.split(",")]
            if line_parts[0] == '' or '**' in line_parts[0] or '#' in line_parts[0]:
                pass            
            else:
                # current_flag setting
                if line_parts[0] == "*End":
                    current_flag = 0                      
                elif line_parts[0] == "*Time":              
                    current_flag = "*Time"                   
                elif   line_parts[0] == "*Element":
                    current_flag = "*Element"
                elif   line_parts[0] == "*ElementInOut":
                    current_flag = "*ElementInOut"
                elif   line_parts[0] == "*ElementPolymer":  
                    current_flag = "*elementPolymer"            
                elif line_parts[0] == "*Reaction": 
                    current_flag, normConst = "*Reaction", line_parts[1]
                    
                # 2025.1.9
                elif line_parts[0] == "*Set01_inter":
                    current_flag = "*Set01_inter"
                    
                elif line_parts[0] == "*ReactionPolymer":   
                    current_flag, normConst = "*ReactionPolymer", line_parts[1]        
                elif line_parts[0] == "*Plot":
                    current_flag = allPlots.plotSetting(line_parts)           
                elif line_parts[0] == "*Comment":
                    current_flag = "*Comment"
                elif line_parts[0] == "*SetDefine":
                    current_flag, setName = "*SetDefine", line_parts[1]
                    print(f"\n In *SetDefine, the Set Name is {setName}. \n")
                    allSets.createSet(setName, allElements, allReactions, allPlots)
                              
                # action list                    
                elif   (current_flag == "*Time") or \
                       (current_flag == "*Element") or \
                       (current_flag == "*ElementInOut") or \
                       (current_flag == "*elementPolymer") or \
                       (current_flag == "*Comment"):                    
                    InputItems[current_flag](line_parts)   # 2022.10.30
                elif current_flag == "*Reaction":
                    subFlg, ls_x = _reactionDefinition(line_parts,
                                                       subFlg,
                                                       normConst,
                                                       allReactions,
                                                       allElements,
                                                       Lines_for_rM)
                    Lines_for_rM.insert(subFlg-1, ls_x)                   
                elif current_flag == "*ReactionPolymer":
                    allReactions.createReactionPolymer(line_parts, allElements, normConst)
                elif current_flag == "*Plot":
                    allPlots.appendList(line_parts, allElements.elements)
                elif current_flag == "*SetDefine":
                    # 2025.1.8
                    allSets.createSet(setName, allElements, allReactions, allPlots)

    
def commentLine(line_parts):
    pass


def _reactionDefinition(line_parts, subFlg, normConst, allReactions, allElements, Lines_for_rM):
    ls_x = ""
    if line_parts[0] == 'rM' and subFlg == 0:
        ls_x = line_parts
        subFlg += 1
    elif subFlg == 1:               
        ls_x = line_parts
        if len(ls_x) == 1 or ls_x[1] == None or ls_x[1] == "":
            ls_x =[ls_x[0], str(normConst)]
        subFlg += 1
    elif subFlg == 2:               
        ls_x = line_parts
        allReactions.setReactionMulti(Lines_for_rM[0], Lines_for_rM[1][0], Lines_for_rM[1][1], ls_x, allElements.elements)
        subFlg = 0
    else:
        allReactions.setReaction(line_parts, allElements.elements, normConst)
    return subFlg, ls_x


def setDefine(newFileName, allElements, allReactions, allPlots, allSets):   
    
    with open(newFileName, encoding="utf-8_sig") as f:   # windows needs encoding="utf-8_sig"
        current_flag = 0
        subFlg = 0
        flgSet = 0  
        setName = ""
        print("\n In def setDefine: ", newFileName)        
    
        for line in f:
            line_new = line.replace('\n','')
            line_parts = [x.strip() for x in line_new.split(",")]
            if line_parts[0] == '' or '**' in line_parts[0] or '#' in line_parts[0]:
                pass            
            else:
                # current_flag setting
                if line_parts[0] == "*End":
                    current_flag = 0 
                elif line_parts[0] == "*SetDefine":              
                    flgSet = "*SetDefine"
                    setName = line_parts[1]
                    print(f"\n In def setDefine(), setName is {setName} \n")
                elif line_parts[0] == "*Element":
                    current_flag = "*Element"
                elif line_parts[0] == "*Reaction": 
                    current_flag = "*Reaction"  
                elif line_parts[0] == "*Plot":
                    current_flag = "*Plot"
                # action
                elif current_flag == "*Element" and flgSet == "*SetDefine":
                    allSets.addSetElements(setName, line_parts[0], allElements)
                    
                elif current_flag == "*Reaction" and flgSet == "*SetDefine":
                    if line_parts[0] == "rM" or subFlg == 0:
                        reactionName = line_parts[0].strip() + '_' + line_parts[1].strip()
                        allSets.addSetReactions(setName, reactionName, allReactions)                        
                        if line_parts[0] == "rM":
                            subFlg += 1
                    elif subFlg == 1:
                        subFlg += 1
                    elif subFlg == 2:
                        subFlg = 0
                    else:  
                        pass
                elif current_flag == "*Plot" and flgSet == "*SetDefine":
                    allSets.addSetPlots(setName, line_parts, allPlots)
