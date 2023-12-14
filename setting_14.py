#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 18:00:04 2022

@author: takashi
"""

import sys
import itertools
import copy

allnewNames = []
allnewNameDict = {}

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
        
    [[[BUG]]] need *End in file at end of *Set_01, *Set_02, and *ReactionExchange 

    '''
    newFileName = fName
    f_main = open(fName, 'r', encoding='UTF-8_sig')
    data_main = f_main.readlines() 
    
    with open(fName, encoding="utf-8_sig") as f:
        setFlg = ""
        setLines_01 = []
        setLines_02 = []
        
        for line in f:
            line_new = line.replace('\n','')
            line_sprit = [x.strip() for x in line_new.split(",")]
            
            if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
                pass
            else:            
                if "*End" in line and setFlg == "*Set_01":
                    setFlg = ""
                    deleteLine(data_main, line)
                if setFlg == "*Set_01":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    setLines_01.append(line_sprit)
                    deleteLine(data_main, line)
                if "*Set_01" in line:
                    setFlg = "*Set_01"  
                    deleteLine(data_main, line)
    
                if "*End" in line and setFlg == "*Set_02":
                    setFlg = ""
                    print(f"*Set_02 is out. line is {line}")
                    deleteLine(data_main, line)                                
                if setFlg == "*Set_02":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    setLines_02.append(line_sprit)
                    print(f"In a line of *Set_02. line: {line}")
                    deleteLine(data_main, line)
                if "*Set_02" in line:
                    setFlg = "*Set_02"
                    print(f"setFlg is *Set_02. line is {line}")
                    deleteLine(data_main, line)

        print("setLines_01: \n", setLines_01)
        print("setLines_02: \n", setLines_02)
    
    newLines_01, newFileName, allnewNameDict = _makeNewFiles(fName, data_main, setLines_01)
    newLines_03 = _makeNewLines_03(newLines_01, newFileName, allnewNameDict)
    print("newLines_03: ", newLines_03)
    newLines_01.extend(newLines_03)
    
    if newLines_01 == []:
        pass
    else:
        _writeNewFile(newLines_01, newFileName)      # temp 2022.12.11
    return newFileName


def deleteLine(data_main, line):
    data_main.remove(line)
    print(f"*** Deleted line is [ {line} ]")


def _makeNewFiles(fName, data_main, setLines_01):
    newLines_01 = []
    newLines_01.append(data_main)
    if setLines_01 == []:
        return [], fName, []
    else:
        for set_line in setLines_01:
            newLines, newNames, newNameDict = _writeNewLines(set_line)
            newLines_01.append(newLines)
            allnewNames.append(newNames)
            allnewNameDict.update(newNameDict)
        newFileName = fName[:-4] + "_new" + ".txt" 
        newLines_01 = list(itertools.chain.from_iterable(newLines_01))  
        print("newFileName is : \n", newFileName)
        print("allnewNames is : \n", allnewNames)
        print("allnewNameDict is : \n", allnewNameDict)
        return newLines_01, newFileName, allnewNameDict

    
def _writeNewLines(set_line):
    newNames = []
    newNameDict = {}
    newLines = []
    print("set_line: ", set_line)
    for n in range(int(set_line[2])):
        newNames.append(set_line[1][:-4] + "_" + str(n + 1))
    print("newNames: \n", newNames)
    newNameDict[set_line[0]] = newNames
    
    f = open(set_line[1], 'r', encoding='UTF-8_sig')
    setFile = f.readlines()
    print("setFile: \n", setFile)
    f.close()    
    for nName in newNames:
        newData = _createNewLines(setFile, nName)
        newLines.append(newData)
    newLines = list(itertools.chain.from_iterable(newLines))    
    return newLines, newNames, newNameDict


def _createNewLines(setFile, nName):
    # 2023.2.19
    newData = ["** *SetDefine, " + nName + "\n", ]      # under constraction
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
      
      
def _makeNewLines_03(newLines_01, newFileName, allnewNameDict): 
    
    newLines_03 = [ ]
    newLines_04 = copy.deepcopy(newLines_01)
    print()
    print("lines in 'def _createNewLines_03': ")
    reFlg = ""
    for line in newLines_04:
        line_sprit = [x.strip() for x in line.split(",")]
        if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
            pass
        else:         
            if '*End' in line_sprit[0]:
                reFlg = ""
                deleteLine(newLines_01, line) 
                
            if "*ReactionExchange" == reFlg:
                newLines = _createNewLine_02(line, allnewNameDict)
                print("newLines: ", newLines)
                for nL in newLines:
                    newLines_03.append(', '.join(nL))  
                deleteLine(newLines_01, line)                           # 2023.2.5
                
            if '*ReactionExchange' == line_sprit[0]:
                reFlg = "*ReactionExchange"
                newLines_03.append("*Reaction" + ", " + line_sprit[1] + ", " + line_sprit[2] + "\n")
                deleteLine(newLines_01, line)                           # 2023.2.5
            elif "*ReactionExchange" != reFlg:
                pass
    return newLines_03

# 2022.12.10
# 2023.2.13 Bug!!
def _createNewLine_02(line, allnewNameDict):
    newLines = []
    line = line.split(",")
    print(line)
    vNew = []
    vKeyWord = ""
    vKeyWordDict = {}             # まだ使用していない
    for ls in line:
        for k, v in allnewNameDict.items():
            if ":=" + k in ls:
                vKeyWord = ":=" + k
                vv = []
                for vn in v:
                    ls_n = ls.replace(":=" + k, ":=" + vn)
                    vv.append(ls_n)
                    vNew.append(ls_n)
                vKeyWordDict[vKeyWord] =  vv

    for i, n in enumerate(vNew):
        nL = []
        for j, ls in enumerate(line):
            if vKeyWord in ls:
                nL.append(n)
            elif j == 1:
                nL.append(ls + "_" + str(i + 1))
            else:
                nL.append(ls)
        newLines.append(nL)
    return newLines


def _writeNewFile(newLines, newFileName):
    with open(newFileName, 'w') as f:
        f.writelines(newLines)


def openReadFile(fName, elms, reacs, timeM, utils, creR, poly, plots):

    InputItems = {"*Time": timeM.setTime, 
                  "*Element": elms.setElement,
                  "*ElementInOut": elms.setElementInOut,
                  "*elementPolymer": elms.setElementPolymer
                  }
    
    with open(fName, encoding="utf-8_sig") as f:   # windows needs encoding="utf-8_sig"
        flg = 0
        subFlg = 0
        normConst = 0
        ls = []     
        print("f in openReadFile: ", fName)
        
        for line in f:
            line_new = line.replace('\n','')
            line_sprit = [x.strip() for x in line_new.split(",")]
            # print(line_sprit)                                          # 2022.12.25
            if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
                pass            
            else:
                # flg setting
                if line_sprit[0] == "*End":
                    flg = 0                      
                elif line_sprit[0] == "*Time":              
                    flg = "*Time"                   
                elif   line_sprit[0] == "*Element":
                    flg = "*Element"
                elif   line_sprit[0] == "*ElementInOut":
                    flg = "*ElementInOut"
                elif   line_sprit[0] == "*ElementPolymer":  
                    flg = "*elementPolymer"            
                elif line_sprit[0] == "*Reaction": 
                    # flg, normConst = reactionSetting(line_sprit)  
                    flg, normConst = reactionSetting_02(line_sprit, elms)
                elif line_sprit[0] == "*ReactionPolymer":   
                    flg = reactionPolymerSetting(line_sprit, reacs)           
                elif line_sprit[0] == "*Plot":
                    flg = plots.plotSetting(line_sprit)           
                elif line_sprit[0] == "*Comment":
                    flg = "*Comment"
                              
                # action list                    
                elif   (flg == "*Time") or \
                       (flg == "*Element") or \
                       (flg == "*ElementInOut") or \
                       (flg == "*elementPolymer"):                           
                    InputItems[flg](line_sprit)   # 2022.10.30
                elif flg == "*Reaction":
                    subFlg, ls_x = \
                        reactionDefinition(line_sprit, subFlg, normConst, reacs, elms, ls)
                    ls.insert(subFlg-1, ls_x)                   
                elif flg == "*ReactionPolymer":
                    creR.createReactionPolymer(line_sprit, elms, reacs)
                elif flg == "*Plot":
                    plots.appendList(line_sprit, elms.allElements)


def reactionSetting(line_sprit):
    try:
        normConst = int(float(line_sprit[1])) 
    except ValueError as e:            
        print("ValueError : ", e)
        print("A number is required in the second term of the *Reaction line.")
        sys.exit()   
    return "*Reaction", normConst


def reactionSetting_02(line_sprit, elms):
    try:
        if line_sprit[1] == "default":
            normConst = 0
            for el in elms.allElements.values():
                normConst += el.n
        else:
            normConst = int(float(line_sprit[1]))
        try:
            if type(float(line_sprit[2])) is float:
                normConst = normConst*float(line_sprit[2])
        except:
            pass                
        print(f"The default N is {normConst}") 
    except ValueError as e:            
        print("ValueError : ", e)
        print("A number is required in the second term of the *Reaction line.")
        sys.exit()   
    return "*Reaction", normConst


def reactionPolymerSetting(line_sprit, reacs):
    reacs.all = int(float(line_sprit[1])) 
    return "*ReactionPolymer"


def reactionDefinition(line_sprit, subFlg, normConst, reacs, elms, ls):
    ls_x = ""
    if line_sprit[0] == 'rM' and subFlg == 0:
        ls_x = line_sprit
        subFlg += 1
    elif subFlg == 1:               
        ls_x = line_sprit
        if len(ls_x) == 1 or ls_x[1] == None or ls_x[1] == "":
            ls_x =[ls_x[0], str(normConst)]
        subFlg += 1
    elif subFlg == 2:               
        ls_x = line_sprit
        print("ls: ", ls)
        reacs.setReactionMulti(ls[0], ls[1], ls_x, elms.allElements)
        subFlg = 0
    else:
        reacs.setReaction(line_sprit, elms.allElements, normConst)
    return subFlg, ls_x


    


