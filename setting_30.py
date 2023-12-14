#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 18:00:04 2022

@author: takashi
"""

import os
import itertools

allnewNameDict = {}
newNameDict_01 = {}
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
        reactionExchangeLine = []
        for line in f:
            line_new = line.replace('\n','')
            line_sprit = [x.strip() for x in line_new.split(",")]
        
            if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
                pass
            else:            
                # setting
                if "*End" in line:
                    setFlg = ""
                    delete_flag = False                
                if "*End" in line and setFlg == "*Set_01":
                    setFlg = ""
                    delete_flag = True
                elif "*Set_01" in line:
                    setFlg = "*Set_01"
                    delete_flag = True
                elif "*End" in line and setFlg == "*Set_02":
                    setFlg = ""
                    delete_flag = True
                elif "*Set_02" in line:
                    setFlg = "*Set_02"
                    delete_flag = True
                elif "*ReactionExchange" in line:
                    setFlg = "*ReactionExchange"
                    delete_flag = True
                # action    
                elif setFlg == "*Set_01":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    setLines_01.append(line_sprit)
                    delete_flag = True
                elif setFlg == "*Set_02":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    setLines_02.append(line_sprit)
                    delete_flag = True
                elif setFlg == "*ReactionExchange":
                    line_new = line.replace('\n','')
                    line_sprit = [x.strip() for x in line_new.split(",")]
                    reactionExchangeLine.append(line_sprit)
                    print(f"In a line of *ReactionExchange. line: \n {line}")
                    delete_flag = True
                else:
                    delete_flag = False
        
                if delete_flag:
                    _prependAsterisk(data_main, line)
                    
    newFileName = _makeNewFileName(fName, setLines_01)
    newLines_01, newNameDict_01 = _makeNewLines_01(data_main, setLines_01)
    print("newLines_01: \n", newLines_01[:100])
    newLines_02, newNameDict_02 = _makeNewLines_02(setLines_02)
    print("newLines_02: \n", newLines_02[:100])
    newLines_01.extend(newLines_02)
    newLines_03 = _makeNewLines_03(reactionExchangeLine, newNameDict_01, newNameDict_02)
    print("newLines_03: \n", newLines_03[:100])
    newLines_01.extend(newLines_03)
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

def _makeNewLines_01(data_main, setLines_01):
    newLines_01 = []
    newLines_01.append(data_main)
    newNameDict_01 = {}
    print("setLines_01: \n", setLines_01)
    for set_line in setLines_01:
        newLines, newNames, newNameDict = _writeNewLines_01(set_line)
        newLines_01.append(newLines)
        newNameDict_01.update(newNameDict)
    newLines_01 = list(itertools.chain.from_iterable(newLines_01)) 
    print("*********** ************")
    print("newNameDict at *Set_01 is : \n", newNameDict_01)
    print("*********** ************")
    return newLines_01, newNameDict_01

def _writeNewLines_01(set_line):
    newNames = []
    newNameDict = {}
    newLines = []
    print("set_line: \n", set_line)
    for n in range(int(set_line[2])):
        newNames.append(set_line[0] + "_" + str(n + 1))
    print("newNames: \n", newNames)
    newNameDict[set_line[0]] = newNames
    
    f = open(set_line[1], 'r', encoding='UTF-8_sig')
    setFile = f.readlines()
    f.close()    
    for nName in newNames:
        newData = _createNewLines_01(setFile, nName)
        newLines.append(newData)
    newLines = list(itertools.chain.from_iterable(newLines))    
    return newLines, newNames, newNameDict

def _createNewLines_01(setFile, nName):
    # 2023.2.19
    newData = [" \n",
               " \n",
               "** ************************************ \n",
               "*SetDefine, " + nName + "\n", 
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

def _makeNewLines_02(setLines_02):
    newLines_02 = []
    newNameDict_02 = {}
    print("setLines_02: \n", setLines_02) 
    for setLine in setLines_02:
        newLines, newNames, newNameDict = _writeNewLines_02(setLine)
        newLines_02.append(newLines)
        newNameDict_02.update(newNameDict)
    newLines_02 = list(itertools.chain.from_iterable(newLines_02))  
    print("*********** ************")
    print("newNameDict_02 at *Set_02 is : \n", newNameDict_02)
    print("*********** ************")
    return newLines_02, newNameDict_02

def _writeNewLines_02(sL):
    print("setLine: \n", sL) 
    newSet = {}
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
        newData = _createNewLines_02(setFile, nName)
        newLines.append(newData)
    newLines = list(itertools.chain.from_iterable(newLines))    
    newSet[setName] = newNames
    return newLines, newNames, newSet

def _createNewLines_02(setFile, nName):
    # 2023.4.29
    newData = ["** ************************************ \n",
                "*SetDefine, " + nName + "\n", 
                "** ************************************ \n"]      # under constraction
    nName_first = nName.split("::")[0]
    nName_second = nName.split("::")[1]
    # print(nName_first, nName_second)
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

def _makeNewLines_03(reactionExchangeLines, newNameDict_01, newNameDict_02):  
    print()
    print("lines in 'def _makeNewLines_03': ")
    if reactionExchangeLines == []:
        newLines_03 = []
    else:
        newLines_03 = [["*Reaction, ",  "default", "\n"]]
        for line in reactionExchangeLines:
            first = False
            second = False
            for ls in line:
                if ":=" in ls:
                    first = True
                if "::" in ls:
                    second = True
            if first == True and second == False:        
                print("In _createNewLines_03_1")
                newLines = _createNewLines_03_1(line, newNameDict_01)
                newLines_03.append(newLines)
            if first == True and second == True: 
                print("In _createNewLines_03_2")
                newLines = _createNewLines_03_2(line, newNameDict_02)
                newLines_03.append(newLines)    
        newLines_03 = list(itertools.chain.from_iterable(newLines_03))  
    return newLines_03

def _createNewLines_03_1(line, newNameDict_01):    # refactoring by ChatGPT4
    newLines = []
    line_copy = line + ["\n"]
    for j in range(len(line) - 1):
        line_copy[j] = line_copy[j] + ", "     
    for i, ls in enumerate(line):
        if ":=" in ls:
            for k, v in newNameDict_01.items():
                for vn in v:
                    newLine = line_copy.copy()
                    newLine[i] = ls.replace(":=", f":={vn}, ")
                    newLine[1] = newLine[1].replace(",", f":={vn}, ")
                    newLines.append(newLine)
    return list(itertools.chain.from_iterable(newLines))

def _createNewLines_03_2(line, newNameDict_02):
    newLines = []
    newLines_2 = []
    line_copy = line + ["\n"]
    for j in range(len(line) - 1):
        line_copy[j] = line_copy[j] + ", "   
    for i, ls in enumerate(line):
        if "::" in ls:
            for k, v in newNameDict_02.items():
                first_name = ""
                for vn in v:
                    newLine = line_copy.copy()
                    newLine[i] = ls.replace("::", f"::{vn}, ")
                    newLine[1] = newLine[1].replace(",", f"::{vn}, ")
                    first_name = vn.split("::")[0]
                    newLines.append(newLine)
    
    for nline in newLines:
        newLine_3 = nline.copy()
        first_name = nline[1].split("::")[1]
        for i, nls in enumerate(nline):
            if ":=" in nls:
                newLine_3[i] = nls.replace(":=", f":={first_name}")
                newLines_2.append(newLine_3)
                print("newLine_3: ", newLine_3)
    return list(itertools.chain.from_iterable(newLines_2))

def _writeNewFile(newLines, newFileName):
    print("def _writeNewFile: ")
    print("newLines: ", newLines[:100])
    with open(newFileName, 'w') as f:
        f.writelines(newLines)

def openReadFile(fName, all_elements, all_reactions, timeM, utils, poly, plots):

    InputItems = {"*Time": timeM.setTime, 
                  "*Element": all_elements.setElement,
                  "*ElementInOut": all_elements.setElementInOut,
                  "*elementPolymer": all_elements.setElementPolymer,
                  "*Comment": commentLine
                  }
    with open(fName, encoding="utf-8_sig") as f:   # windows needs encoding="utf-8_sig"
        flg = 0
        subFlg = 0#!/
        normConst = 0
        Lines_for_rM = []     
        print("f in openReadFile: ", fName)
        
        for line in f:
            line_new = line.replace('\n','')
            line_sprit = [x.strip() for x in line_new.split(",")]
            if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
                pass            
            else:
                # flg setting
                if line_sprit[0] == "*End" or line_sprit[0] == "*SetDefine" :
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
                    flg, normConst = "*Reaction", line_sprit[1]
                elif line_sprit[0] == "*ReactionPolymer":   
                    flg, normConst = "*ReactionPolymer", line_sprit[1]        
                elif line_sprit[0] == "*Plot":
                    flg = plots.plotSetting(line_sprit)           
                elif line_sprit[0] == "*Comment":
                    flg = "*Comment"
                              
                # action list                    
                elif   (flg == "*Time") or \
                       (flg == "*Element") or \
                       (flg == "*ElementInOut") or \
                       (flg == "*elementPolymer") or \
                       (flg == "*Comment"):                    
                    InputItems[flg](line_sprit)   # 2022.10.30
                elif flg == "*Reaction":
                    subFlg, ls_x = _reactionDefinition(line_sprit,
                                                       subFlg,
                                                       normConst,
                                                       all_reactions,
                                                       all_elements,
                                                       Lines_for_rM)
                    Lines_for_rM.insert(subFlg-1, ls_x)                   
                elif flg == "*ReactionPolymer":
                    all_reactions.createReactionPolymer(line_sprit, all_elements, normConst)
                elif flg == "*Plot":
                    plots.appendList(line_sprit, all_elements.elements)
    f.close()
    
def commentLine(line_sprit):
    # print("def commentLine(line_sprit):")
    pass

def _reactionDefinition(line_sprit, subFlg, normConst, all_reactions, all_elements, Lines_for_rM):
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
        print("ls_x: ", ls_x)
        all_reactions.setReactionMulti(Lines_for_rM[0], Lines_for_rM[1][0], Lines_for_rM[1][1], ls_x, all_elements.elements)
        subFlg = 0
    else:
        all_reactions.setReaction(line_sprit, all_elements.elements, normConst)
    return subFlg, ls_x


def setDefine(newFileName, all_elem, all_react, all_plot, all_set):   
    
    with open(newFileName, encoding="utf-8_sig") as f:   # windows needs encoding="utf-8_sig"
        flg = 0
        subFlg = 0
        flgSet = 0  
        setName = ""
        print("f in openReadFile: ", newFileName)        
    
        for line in f:
            line_new = line.replace('\n','')
            line_sprit = [x.strip() for x in line_new.split(",")]
            if line_sprit[0] == '' or '**' in line_sprit[0] or '#' in line_sprit[0]:
                pass            
            else:
                # flg setting
                if line_sprit[0] == "*End":
                    flg = 0 
                elif line_sprit[0] == "*SetDefine":              
                    flgSet = "*SetDefine"
                    setName = line_sprit[1]
                    all_set.createSet(setName)
                    # print("*SetDefine: ", setName)
                elif   line_sprit[0] == "*Element":
                    flg = "*Element"
                elif line_sprit[0] == "*Reaction": 
                    flg = "*Reaction"  
                elif line_sprit[0] == "*Plot":
                    flg = "*Plot"
                # action
                elif flg == "*Element" and flgSet == "*SetDefine":
                    all_set.addSetElements(setName, line_sprit[0], all_elem)
                    
                elif flg == "*Reaction" and flgSet == "*SetDefine":
                    if line_sprit[0] == "rM" and subFlg == 0:
                        rName = line_sprit[0] + "_" + line_sprit[1]
                        subFlg += 1
                    elif subFlg == 1:
                        subFlg += 1
                    elif subFlg == 2:
                        subFlg = 0
                    else:  
                        pass
                elif flg == "*Plot" and flgSet == "*SetDefine":
                    pass
    f.close()

def writeRestartFile(fName, all_elements):
    print("In writeRestartFile()")
    updated_lines = []
    is_element_section = False
  
    with open(fName, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            items = line.split(', ')
            
            if line.startswith('*Element') or line.startswith('*ElementInOut'):
                is_element_section = True
            elif line.startswith('*Time') or line.startswith('*Reaction') or line.startswith('*Plot'):
                is_element_section = False            
            
            if is_element_section:
                if items[0] in all_elements.elements:
                    updated_n = all_elements.elements[items[0]].getN()
                    items[1] = str(updated_n)
                    updated_line = ', '.join(items)
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

    os.chdir("..") 
    with open(fName[:-4] + "_Re" + ".txt", 'w') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')   
    pass
