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
    
    
def writeRestartFile(fName, allElements):
    print("\n !!! In writeRestartFile( ) !!!")
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
                if items[0] in allElements.elements:
                    updated_n = allElements.elements[items[0]].currentNums[-1]       # 2023.11.26 -> 2024.10.4
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
    

def writeRestartFile_new5(fName, allElements):
    """
    Generate a restart file, ensuring that *SetDefine lines are commented out.
    
    Parameters:
    - fName (str): The input file name.
    - allElements (AllElements): The object containing element definitions.
    """

    print("\n !!! In writeRestartFile( ) !!!")
    updated_lines = []  # Stores the updated lines for the restart file
    is_element_section = False
    is_reaction_section = False
    is_plot_section = False
    # set_definitions = {}

    with open(fName, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            items = line.split(', ')

            # Determine the section of the file
            if line.startswith('*Element') or line.startswith('*ElementInOut'):
                is_element_section = True
                is_reaction_section = False
                is_plot_section = False
            elif line.startswith('*Reaction'):
                is_reaction_section = True
                is_element_section = False
                is_plot_section = False
            elif line.startswith('*Plot'):
                is_plot_section = True
                is_element_section = False
                is_reaction_section = False
            elif line.startswith('*SetDefine'):
                # Comment out *SetDefine lines
                updated_lines.append(f"** {line}")
                continue  # Skip further processing of this line
            elif line.startswith('*Time'):
                is_element_section = False
                is_reaction_section = False
                is_plot_section = False

            # Process each section
            if is_element_section:
                original_name = items[0]
                updated_name = original_name

                # Check if the name exists in any element's name_history
                for element in allElements.elements.values():
                    if original_name in element.name_history:
                        updated_name = element.name
                        break

                # Update the name and quantity if the name was changed
                if updated_name in allElements.elements:
                    updated_n = allElements.elements[updated_name].currentNums[-1]
                    items[0] = updated_name
                    items[1] = str(updated_n)
                    updated_line = ', '.join(items)
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)

            elif is_reaction_section:
                updated_items = []
                for item in items:
                    updated_item = item
                    for element in allElements.elements.values():
                        if item in element.name_history:
                            updated_item = element.name
                            break
                    updated_items.append(updated_item)

                updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            elif is_plot_section:
                updated_items = []
                for item in items:
                    updated_item = item
                    for element in allElements.elements.values():
                        if item in element.name_history:
                            updated_item = element.name
                            break
                    updated_items.append(updated_item)

                updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            else:
                updated_lines.append(line)

    # Write the updated lines to a new restart file
    os.chdir("..") 
    new_file_name = fName[:-4] + "_Re" + ".txt"
    with open(new_file_name, 'w') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')
    
    print(f"Restart file written to {new_file_name}")



def writeRestartFile_new6(fName, allElements):
    """
    Generate a restart file, ensuring that *SetDefine lines are commented out.

    Parameters:
    - fName (str): The input file name.
    - allElements (AllElements): The object containing element definitions.
    """

    print("\n !!! In writeRestartFile( ) !!!")
    updated_lines = []  # Stores the updated lines for the restart file
    is_element_section = False
    is_reaction_section = False
    is_plot_section = False
    setName = ""  # To store the current set name for *SetDefine lines

    with open(fName, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            items = line.split(', ')

            # Determine the section of the file
            if line.startswith('*Element') or line.startswith('*ElementInOut'):
                is_element_section = True
                is_reaction_section = False
                is_plot_section = False
            elif line.startswith('*Reaction'):
                is_reaction_section = True
                is_element_section = False
                is_plot_section = False
            elif line.startswith('*Plot'):
                is_plot_section = True
                is_element_section = False
                is_reaction_section = False
            elif line.startswith('*SetDefine'):
                # Extract the set name from the *SetDefine line
                setName_parts = line.split(', ')
                if len(setName_parts) > 0:
                    setName = setName_parts[1].strip()
                # Comment out *SetDefine lines
                updated_lines.append(f"** {line}")
                continue  # Skip further processing of this line
            elif line.startswith('*Time'):
                is_element_section = False
                is_reaction_section = False
                is_plot_section = False

            # Process each section
            if is_element_section:
                original_name = items[0]
                updated_name = original_name

                # Check if the name exists in any element's name_history
                for element in allElements.elements.values():
                    if original_name in element.name_history:
                        updated_name = element.name
                        break

                # Update the name and quantity if the name was changed
                if updated_name in allElements.elements:
                    updated_n = allElements.elements[updated_name].currentNums[-1]
                    items[0] = updated_name
                    items[1] = str(updated_n)
                    updated_line = ', '.join(items)
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)

            elif is_reaction_section:
                updated_items = []
                if "*Reaction" in items:
                    updated_line = items 
                else:
                    for i, item in enumerate(items):
                        if i == 1:  # Append setName to the second item if setName exists
                            if setName and setName not in item:
                                item = item + setName
                        updated_item = item
                        for element in allElements.elements.values():
                            if item in element.name_history:
                                updated_item = element.name
                                break
                        updated_items.append(updated_item)
    
                    updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            elif is_plot_section:
                updated_items = []
                for item in items:
                    updated_item = item
                    for element in allElements.elements.values():
                        if item in element.name_history:
                            updated_item = element.name
                            break
                    updated_items.append(updated_item)

                updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            else:
                updated_lines.append(line)

    # Write the updated lines to a new restart file
    os.chdir("..") 
    new_file_name = fName[:-4] + "_Re" + ".txt"
    with open(new_file_name, 'w') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')

    print(f"Restart file written to {new_file_name}")
    


def writeRestartFile_new7(fName, allElements):
    """
    Generate a restart file, ensuring that *SetDefine lines are commented out.

    Parameters:
    - fName (str): The input file name.
    - allElements (AllElements): The object containing element definitions.
    """

    print("\n !!! In writeRestartFile( ) !!!")
    updated_lines = []  # Stores the updated lines for the restart file
    is_element_section = False
    is_reaction_section = False
    is_plot_section = False
    setName = ""  # To store the current set name for *SetDefine lines

    with open(fName, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            items = line.split(', ')

            # Determine the section of the file
            if line.startswith('*Element') or line.startswith('*ElementInOut'):
                is_element_section = True
                is_reaction_section = False
                is_plot_section = False
            elif line.startswith('*Reaction'):
                is_reaction_section = True
                is_element_section = False
                is_plot_section = False
                # Keep the reaction header line unchanged
                updated_lines.append(line)
                continue
            elif line.startswith('*Plot'):
                is_plot_section = True
                is_element_section = False
                is_reaction_section = False
            elif line.startswith('*SetDefine'):
                # Extract the set name from the *SetDefine line
                setName_parts = line.split(', ')
                if len(setName_parts) > 0:
                    setName = setName_parts[1].strip()
                # Comment out *SetDefine lines
                updated_lines.append(f"** {line}")
                continue  # Skip further processing of this line
            elif line.startswith('*Time'):
                is_element_section = False
                is_reaction_section = False
                is_plot_section = False

            # Process each section
            if is_element_section:
                original_name = items[0]
                updated_name = original_name

                # Check if the name exists in any element's name_history
                for element in allElements.elements.values():
                    if original_name in element.name_history:
                        updated_name = element.name
                        break

                # Update the name and quantity if the name was changed
                if updated_name in allElements.elements:
                    updated_n = allElements.elements[updated_name].currentNums[-1]
                    items[0] = updated_name
                    items[1] = str(updated_n)
                    updated_line = ', '.join(items)
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)

            elif is_reaction_section:
                updated_items = []
                for i, item in enumerate(items):
                    if i == 1:  # Append setName to the second item if setName exists
                        if setName and setName not in item:
                            item = item + setName
                    updated_item = item
                    for element in allElements.elements.values():
                        if item in element.name_history:
                            updated_item = element.name
                            break
                    updated_items.append(updated_item)

                updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            elif is_plot_section:
                updated_items = []
                for item in items:
                    updated_item = item
                    for element in allElements.elements.values():
                        if item in element.name_history:
                            updated_item = element.name
                            break
                    updated_items.append(updated_item)

                updated_line = ', '.join(updated_items)
                updated_lines.append(updated_line)

            else:
                updated_lines.append(line)

    # Write the updated lines to a new restart file
    os.chdir("..") 
    new_file_name = fName[:-4] + "_Re" + ".txt"
    with open(new_file_name, 'w') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')

    print(f"Restart file written to {new_file_name}")

# under constraction    
def compareRestartFileWithObjects(restart_file, allElements, allReactions, allPlots, report_file="comparison_report.txt"):
    """
    Compare the content of a restart file with AllElements, AllReactions, and AllPlots objects,
    and output a report highlighting inconsistencies.

    Parameters:
    - restart_file (str): Path to the restart file.
    - allElements (AllElements): Object containing element definitions.
    - allReactions (AllReactions): Object containing reaction definitions.
    - allPlots (AllPlots): Object containing plot definitions.
    - report_file (str): Path to the output report file.
    """

    print("\n !!! Comparing restart file with objects !!!")
    element_names = set(allElements.elements.keys())
    reaction_names = set(allReactions.reactions.keys())

    # Extract all plot element names from AllPlots
    plot_names = set()
    for plot in allPlots.allPlots:
        for element in plot.plotList:
            plot_names.add(element.name)

    missing_elements = []
    missing_reactions = []
    missing_plots = []

    with open(restart_file, 'r') as file:
        lines = file.readlines()

        current_section = None

        for line in lines:
            line = line.strip()

            # Determine the section of the file
            if line.startswith('*Element') or line.startswith('*ElementInOut'):
                current_section = 'element'
                continue
            elif line.startswith('*Reaction'):
                current_section = 'reaction'
                continue
            elif line.startswith('*Plot'):
                current_section = 'plot'
                continue
            elif line.startswith('*Time'):
                current_section = None
                continue

            # Check consistency based on the current section
            if current_section == 'element':
                # Extract element name from the line
                element_name = line.split(', ')[0]
                if element_name not in element_names:
                    missing_elements.append(element_name)
            elif current_section == 'reaction':
                # Extract reaction name from the line
                reaction_name = line.split(', ')[0]
                if reaction_name not in reaction_names:
                    missing_reactions.append(reaction_name)
            elif current_section == 'plot':
                # Extract plot items from the line
                plot_items = line.split(', ')
                for plot_name in plot_items:
                    if plot_name not in plot_names:
                        missing_plots.append(plot_name)

    # Generate report
    with open(report_file, 'w') as report:
        report.write("Comparison Report\n")
        report.write("=================\n\n")

        # Report missing elements
        if missing_elements:
            report.write("Missing Elements:\n")
            report.write("------------------\n")
            for element in missing_elements:
                report.write(f"{element}\n")
        else:
            report.write("All elements are consistent.\n")
        report.write("\n")

        # Report missing reactions
        if missing_reactions:
            report.write("Missing Reactions:\n")
            report.write("-------------------\n")
            for reaction in missing_reactions:
                report.write(f"{reaction}\n")
        else:
            report.write("All reactions are consistent.\n")
        report.write("\n")

        # Report missing plots
        if missing_plots:
            report.write("Missing Plots:\n")
            report.write("--------------\n")
            for plot in missing_plots:
                report.write(f"{plot}\n")
        else:
            report.write("All plots are consistent.\n")
        report.write("\n")

    print(f"Comparison completed. Report written to {report_file}")