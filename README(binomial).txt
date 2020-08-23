Binomial

--Natural Number Simulation Algorithm for Complex System--


Description

 This python program provides a natural number algorism to simulate complex systems. The number means molecular numbers, cell numbers, polulation numbers, etc. This program contains time evolution simulation code for those natural numbers. You can use this program instead of conventional ordinary differencial equation. Ordinary differencial equations(OEDs) can present phenomenon of vourious numerical systems. This code can solve those numerical systems based on the natural number. OEDs handle real number. However, this code only manages natural number. This featuer enables writing simple code, non-stopping algorism.
You can enjoy this smart algorism.    


Categories

 complex system, system biorogy, A-life, simulation 


File structuer

 This program uses four python files and one input file as shown below.

    1. NNSA.py
        This is main program. This contains reading process of input file and 
        main loop of calculation. 
    2. element.py
        The element class define elements for calculation. For example elements
        are molecules, various cells, and living individuals, etc.
    3. reaction.py
        Classes in the file define several reactions scheme depend on elements.
         Set of input elements and created elements chose a reaction type.
    4. utility.py
         This program contains plotting utility methods.
    5. input.txt (any name is available.)
         This program needs one input file writed by plane text file. 
         To run the program you need to chane input file name in the program. 

 The program developed by Spyder 4.1.4 at Aug 2020.

  

Getting started

         One thing you need to run the program is creating one input file. 
      The file should have four sections, *Time, *Element, *Reaction, and *Plot.
      Locate five files in one folder and run the main program, NNSA.py. Calculation start, and Plots appeare. 
   
    1. Time
           This section is simple. You need to write start time, end time, 
         and console-print-intercal time. You can only write natural numbers. 
         The zero, 0 is available. Calculation performs at interval one, 1.
           
         Format:
         *Time, start time, end time, console print intercal time
        Example:
         *Time, 0, 20000, 1000  

    2. Element
           In this section, you write component items you want to simulate. 
         The name, initial number, color for plotting are necessary. Total
         element numbers needs in the first line.
 
         Format:
          *Element, element numbers
          Name, initial number,  color
           --- --- --- 
           --- --- --- 
          *Element End

        Example:
          *Element, 12
           virus , 500, Black 
           cell, 100000, Green
           virusCell, 0, Yellow
           new_Virus , 0, Gray 
           macrophage, 5000, Orange
           macrophageActive, 0, Green 
           macrophageWithVirus, 0, Yellow
           dendricCell, 500, Blue
           dendricMHC, 0, Red
           IFN, 0, Blue 
           naiveTh1, 100, Green 
           activeTh1, 0, Gray 
         *Element End


    3. Reaction
          This section defines reaction types for those elements defined above. 
        There are five types of the reaction as below.

              r1_2 : One element type separate two kind of element type.
              r1_1 : One element type change to anothor element type. 
              r1_0 : One element type disappeares. 
              r2_2 : Two element types change anothor two element types.
              r2_1 : Two element types become one elementtype.
        
          All reaction also need information that how many element react in the 
        reaction. For example, one element of type A becomes two element of  
        type X and type Y, you write as follows
                   r1_2, 001, 1, A, 0.5, 1, X, 1, Y
        The first term is reaction type, second is a local name, and 0.5 is 
        a reaction parameter. “1, A” is reaction order and element name,
       “1, X, 1, Y” are products’. Reaction orders have to be natural number. 
       Element names have to be defined in the *Element items. 
       In the case of r2_2 and r2_1, a global parameter is necessary. 
       This parameter controls reaction probabilities 
       in reaction r2_2 and r2_1. The reaction parameter and global parameter 
       may be real numbers. In the format below, A, B, X, Y are element name
      defined in the *Element items. The p stand for a propability parameter of
      those reactions. 

         Format:
          *Reaction, reaction numbers, global parameter
           r1_2, name, a, A, p, x, X, y, Y
           r1_1, name, a, A, p, x, X
           r1_0, name, a, A, p
           r2_2, name, a, A, b, B, p, x, X, y, Y
           r2_1, name, a, A, b, B, p, x, X
           --- --- --- 
           --- --- --- 
          *Element End

        Example:
          *Reaction, 13, 1000000
           r1_1, 001, 1, virusCell, 0.07, 2, new_Virus
           r1_1, 002, 1, new_Virus, 0.02, 1, virus
           r1_1, 003, 1, macrophageWithVirus, 0.9, 1, macrophage
           r1_1, 004, 1, dendricMHC, 0.0002, 1, dendricCell
           r1_1, 005, 1, macrophageActive, 0.002, 1, macrophage
           r1_1, 006, 1, activeTh1, 0.001, 1, naiveTh1
           r1_0, 007, 1, IFN, 0.01
           r1_2, 001, 1, activeTh1, 0.6, 2, IFN, 1, activeTh1
           r2_1, 001, 1, virus, 1, cell, 0.0075, 1, virusCell
           r2_1, 002, 1, virus, 1, dendricCell, 0.15, 1, dendricMHC
           r2_1, 003, 1, macrophageActive, 1, virus, 3.0, 1, macrophageWithVirus
           r2_1, 004, 1, macrophage, 2, IFN, 2.0, 1, macrophageActive
           r2_2, 001, 1, naiveTh1, 1, dendricMHC, 0.3, 1, activeTh1, 1, dendricMHC
          *Reaction End
    
    4. Plot
       This section defines plot sets. Elements written in the same line show
     plot in a figuer. A plot number needs to define this section. 
         
         Format:
          *Plot, plot number
           A, X, Y
           B, W
           F
           --- --- --- 
           --- --- --- 
          *Plot End           
    
        Example:
          *Plot, 6
           virus, new_Virus
           cell
           macrophage, macrophageActive, macrophageWithVirus
           dendricMHC, dendricCell
           IFN
           activeTh1, naiveTh1
          *Plot End
