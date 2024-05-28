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
from decimal import Decimal, InvalidOperation


def _load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

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


def _is_integer2(decimal_number):
    # return decimal_number > 0 and decimal_number == int(decimal_number)
    return decimal_number == int(decimal_number)

def convert_to_int2(input_str):
    # Attempt to directly convert input to int
    try:
        return int(input_str)
    except ValueError:
        pass  # Proceed to next attempt if it fails
    
    # Attempt to convert scientific notation to int
    try:
        decimal_number = Decimal(input_str)
        if _is_integer2(decimal_number):
            return int(decimal_number)
        else:
            raise ValueError("Input is not a positive integer.")
    except (InvalidOperation, ValueError):
        pass  # Proceed to next attempt if it fails
    
    # Attempt to convert "base*10**exponent" format to int
    parts = input_str.split('*10**')
    if len(parts) == 2:
        base, exponent = parts
        try:
            base = float(base)  # 使用 float で基数を解釈
            exponent = int(exponent)  # 指数は int で解釈
            result = base * (10 ** exponent)
            if _is_integer2(result):
                return int(result)
            else:
                raise ValueError("Resulting number is not a positive integer.")
        except (ValueError, OverflowError) as e:
            print(e)
            sys.exit(1)
    
    # If all attempts fail, inform the user
    raise ValueError("Input cannot be converted to an integer without rounding.")


