# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# From value_test_02.py

import sys, os
import json
import glob
import platform

from decimal import Decimal

global config, EntropyCalc, CSV_OUTPUT, FIG_OUTPUT, RestartFile


def _load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def init(filename):
    global config, EntropyCalc, CSV_OUTPUT, FIG_OUTPUT, RestartFile
    config = _load_config(filename)
    EntropyCalc = config["settings"]["EntropyCalc"]
    CSV_OUTPUT = config["settings"]["CSV_OUTPUT"]
    FIG_OUTPUT = config["settings"]["FIG_OUTPUT"]
    RestartFile = config["settings"]["RestartFile"]


def setFromTerminal(fName, ShowFigure):
    try:
        fName = sys.argv[1]
        print(f"A input file {fName} is read from terminal.")
        ShowFigure = "NO"
    except:
        pass
    
    if ShowFigure =="YES":
        try:
            print("fName: ", fName)
            print(f"A input file {fName} is read from Spyder.")
        except:
            print("You need one input file.")
            sys.exit()
        
    return fName, ShowFigure


def changeDirectory_to_inputFile(fName):
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

def _is_integer(decimal_number):
    return decimal_number % round(decimal_number) == 0

def convert_to_int(input_str):
    
    return_int = -1
    # print("input_str: ", input_str)
    
    try:
        # Check integer
        return_int = int(input_str)
        # print("return_int  @try 1st: ", return_int)
    except ValueError:
        pass
    
    if return_int == -1:
        try:
            # Check "1.541245787e25" type
            decimal_number = Decimal(input_str)
    
            # Check int
            if not _is_integer(decimal_number):
                print("Error: Cannot convert to integer without rounding. @try 2nd")
                sys.exit()
            else:
                return_int = int(decimal_number)
                # print("return_int  @try 2nd: ", return_int)
        except:
            pass
    else:
        pass
    
    if return_int == -1:
        try:
            # Check 1.547*10**50" type
            parts = input_str.split('*10**')
            if len(parts) == 2:
                base, exponent = parts
                input_str = str(base) + "e" + str(exponent)
                decimal_number = Decimal(input_str)
                # Check int
                if not _is_integer(decimal_number):
                    print("Error: Cannot convert to integer without rounding. @try 3rd")
                    sys.exit()
                else:
                    return_int =  int(decimal_number)
                    # print("return_int  @try 3rd: ", return_int)
            else:
                raise ValueError("Invalid input format. Do you write strings? A number is correct." )
        except ValueError as e:
            print(e)
            sys.exit()
    else:
        pass            
        
    return return_int



