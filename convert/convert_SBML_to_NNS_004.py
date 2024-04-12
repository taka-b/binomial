# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 21:57:19 2024

@author: Takashi Sato
"""

"""
MIT License

Copyright (c) 2024 Takashi Sato

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import libsbml

"""
This section of the program allows for customization of the SBML to NNS (Natural Number Simulation) file conversion process. 
By adjusting the parameters below, users can tailor the conversion to fit specific requirements and configurations. 
Each parameter is designed to control different aspects of the conversion, such as input and output file names, 
simulation timing, initial element quantities, rate constants, and plotting options. 
Please review and modify the parameters as necessary to suit your simulation needs.
"""

# Write the name of the xml file you want to convert to a file for NNS.
filename = "binding_A_B.xml"
filename = sys.argv[1] if len(sys.argv) > 1 else filename

# Change the name of the text file for NNS if you needed.
output_filename = f'{filename[:-4]}_NNS.txt'

# Change the next strings if you change the calculation schedule. 
TIME_SCHEDULE = "0, 100, 10, 50, 1, seconds\n\n"

# If ELEMENT_SETTING is "YES", the initial numbers of the elements set to be INITIAL_NUMBERS.
# If ELEMENT_SETTING is "NO", the initial numbers of the elements set to be from the SBML file.
# However, INITIAL_NUMBERS is set, if we have no the initial numbers in the file.
ELEMENT_SETTING = "NO"
INITIAL_NUMBERS = 999 

# Set the rate constant in the NNS file to RATE_CONSTANT.
# If the rate constant for a reaction is not explicitly defined in the SBML file, this RATE_CONSTANT will be used.
RATE_CONSTANT = 999

# Set the normalization constant in the NNS file to NORMALIZATION_CONSTANT.
NORMALIZATION_CONSTANT = 9.9e9

# Set the plot condition. The "YES" defines the all elements plot in NNS.
# NUMBER_TO_PLOT defines the numbers of elements in one figuer.
# If "NO", the *Plot line is blank.
PLOT_CONDITION = "YES" 
NUMBER_TO_PLOT = 5

def format_rule_component(component):
    """
    Format the components of the reaction rule（example: "1, G1R"）。
    """
    return f"1, {component.strip()}"

def format_total_rule(rule_math):
    """
    Format the reaction expression from the assignment rule.
    """
    # Convert expressions from MathML to text
    rule_str = libsbml.formulaToString(rule_math)
    
    # Split the expression with '+' and format each component
    components = rule_str.split('+')
    formatted_components = [format_rule_component(component) for component in components]
    
    # Generate formatted reaction equations
    reaction_str = ', '.join(formatted_components)
    return reaction_str

def extract_and_format_rules(file_path):
    document = libsbml.readSBMLFromFile(file_path)
    model = document.getModel()
    
    rules_formatted = []

    # Read assignment rules and format
    for rule in model.getListOfRules():
        if rule.isAssignment():
            variable = rule.getVariable()
            math = rule.getMath()
            # Format rules and add to output list
            formatted_rule = f"{format_total_rule(math)} = 1, {variable}"
            rules_formatted.append(formatted_rule)
    
    return rules_formatted

def format_inverse_reaction(reactants, products, k, reaction_id, modifiers):
    inverse_reaction_id = f"{reaction_id}_rev"
    # Combining reactants and modifiers
    combined_reactants = reactants + modifiers
    combined_products = products + modifiers

    # Adjust conditions for using rM format
    if len(combined_reactants) > 4 or len(combined_products) > 4:
        # Special case (rM format)
        reactants_str = f"rM, {inverse_reaction_id}, " + ", ".join([f"1, {species}" for stoichiometry, species in combined_products])  # 逆にする
        kinetics_str = f"{k}"
        products_str = ", ".join([f"1, {species}" for stoichiometry, species in combined_reactants])  # reverse
    else:
        # Normal case
        reactants_str = ", ".join([f"{stoichiometry}, {species}" for stoichiometry, species in combined_products])  # reverse
        products_str = ", ".join([f"{stoichiometry}, {species}" for stoichiometry, species in combined_reactants])  # reverse
        inverse_reaction_type = f"r{len(combined_products)}_{len(combined_reactants)}"
        return f"{inverse_reaction_type}, {inverse_reaction_id}, {reactants_str}, {k}, {products_str}"

    return "\n".join([reactants_str, kinetics_str, products_str])


def format_reaction_component(species, stoichiometry):
    # If stoichiometry is a float, check if it is an integer value
    if isinstance(stoichiometry, float):
        stoichiometry = 1 if not stoichiometry.is_integer() else int(stoichiometry)
    # If stoichiometry is int, use as is
    elif isinstance(stoichiometry, int):
        stoichiometry = stoichiometry
    else:
        # Output error or set default value for unexpected types
        print(f"Warning: Unexpected stoichiometry type for {species}. Setting stoichiometry to 1.")
        stoichiometry = 1
    return f"{stoichiometry}, {species}"

def format_special_reaction(reactants, products, k, unique_name, modifiers):
    # Add reactants and modifiers (catalysts)
    reactants_str = [f'rM, {unique_name}'] + \
        [format_reaction_component(species, stoichiometry) for stoichiometry, species in reactants + modifiers]
    
    # Add modifiers (catalysts) to products as well
    products_str = [format_reaction_component(species, stoichiometry) for stoichiometry, species in products + modifiers]
    
    # Assemble a reaction equation
    return "\n".join([", ".join(reactants_str), f"{k}", ", ".join(products_str)])

def format_reaction(reactants, products, modifiers, k, reaction_index):
    unique_name = reaction_index
    reactant_count = len(reactants) + len(modifiers)  # Number of reactants containing modifiers
    product_count = len(products) + len(modifiers)  # Number of products containing modifiers
    
    if reactant_count == 0:
        # For generative reactions, insert unique name immediately after r1_+.
        formatted_components = [f"r1_+, {unique_name}, 0, 0", f"{k}"]
        formatted_components += [format_reaction_component(species, stoichiometry) for stoichiometry,\
                                 species in products]
    elif product_count == 0:
        # For vanishing reactions, insert the unique name immediately after r1_- and add 0, 0 at the end
        formatted_components = [f"r1_-, {unique_name}"] + \
            [format_reaction_component(species, stoichiometry) for stoichiometry, species in reactants]
        formatted_components += [f"{k}", "0, 0"]
    elif reactant_count > 3 or product_count > 3:
        # Special format response
        return format_special_reaction(reactants, products, k, unique_name, modifiers)
    else:
        # Other reactions, insert unique name immediately after reaction type
        reaction_type = f"r{reactant_count}_{product_count}"
        formatted_components = [f"{reaction_type}, {unique_name}"]

        # Add reactants
        for stoichiometry, species in reactants + modifiers:  # Add modifiers to the reactant list
            formatted_components.append(format_reaction_component(species, stoichiometry))

        formatted_components.append(f"{k}")

        # Adding products
        for stoichiometry, species in products + modifiers:  # Add modifiers to the product list
            formatted_components.append(format_reaction_component(species, stoichiometry))

    return ', '.join(formatted_components).strip()

    # Add reactants
    for stoichiometry, species in reactants + modifiers:  # Add modifiers to the reactant list
        formatted_components.append(format_reaction_component(species, stoichiometry))

    formatted_components.append(f"{k}")

    # Adding products
    for stoichiometry, species in products + modifiers:  # Add modifiers to the product list
        formatted_components.append(format_reaction_component(species, stoichiometry))

    return ', '.join(formatted_components).strip()

def read_sbml_and_extract_reactions_with_kinetics_and_species_initial_values(file_name):
    document = libsbml.readSBMLFromFile(file_name)
    model = document.getModel()
    
    species_list_with_initial_values = []
    for species in model.getListOfSpecies():
        if ELEMENT_SETTING == "YES":
            initial_value = INITIAL_NUMBERS  # Set default values here
        else:    
            if species.isSetInitialConcentration():
                initial_value = species.getInitialConcentration()
            elif species.isSetInitialAmount():
                initial_value = species.getInitialAmount()
            else:
                # If no default value is set, use default value
                initial_value = INITIAL_NUMBERS  # Set default values here
        species_list_with_initial_values.append((species.getId(), initial_value))

    reactions_formatted = []
    
    for i, reaction in enumerate(model.getListOfReactions()):        
        reactants = [(reactant.getStoichiometry(), reactant.getSpecies()) for reactant in reaction.getListOfReactants()]
        products = [(product.getStoichiometry(), product.getSpecies()) for product in reaction.getListOfProducts()]
        modifiers = [(1, modifier.getSpecies()) for modifier in reaction.getListOfModifiers()]
        kinetic_law = reaction.getKineticLaw()
        k = kinetic_law.getParameter(0).getValue() if kinetic_law and kinetic_law.getNumParameters() > 0 else RATE_CONSTANT
        
        reaction_id = reaction.getId()  # Get reaction ID
        reaction_str = format_reaction(reactants, products, modifiers, k, reaction_id)  # Passing on the ID of the response
        reactions_formatted.append(reaction_str)
        
        # For reversible reactions, reverse reactions are also formatted and added, including modifiers
        if reaction.getReversible():
            inverse_reaction_str = format_inverse_reaction(reactants, products, k, reaction_id, modifiers)
            reactions_formatted.append(inverse_reaction_str)

    return species_list_with_initial_values, reactions_formatted


if __name__ == "__main__":
    species_list_with_initial_values, reactions_formatted =\
        read_sbml_and_extract_reactions_with_kinetics_and_species_initial_values(filename)

    rules_formatted = extract_and_format_rules(filename)
    
    with open(output_filename, 'w') as file:
        file.write(f"# A text file for NNS from SBML: {filename}\n\n")
        file.write("*Time\n")
        file.write(TIME_SCHEDULE)
        
        file.write("*Element\n")        
        for species, initial_value in species_list_with_initial_values:
            file.write(f"{species}, {initial_value}\n")
        
        file.write(f"\n*Reaction, {NORMALIZATION_CONSTANT}\n")    
        for reaction_str in reactions_formatted:
            file.write(f"{reaction_str}\n")
        
        file.write("\n*Plot, log\n")
        if PLOT_CONDITION == "YES":
            elements_written = 0
            for species, _ in species_list_with_initial_values:
                file.write(f"{species}")
                elements_written += 1
                # element for each NUMBER_TO_PLOT, or a new line if it is the last element
                if elements_written % NUMBER_TO_PLOT == 0 or elements_written == len(species_list_with_initial_values):
                    file.write("\n")
                else:
                    file.write(", ")  # Write more elements on the same line
        else:
            file.write("\n")
        
        
        file.write("\n# Those are rules in SBML file.\n")
        file.write("# However, the NNS does not have rules for these, so they are commented out.\n\n")        
        for rule_str in rules_formatted:
            file.write(f"# {rule_str}\n")
