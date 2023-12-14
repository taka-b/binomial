Binomial

--- Natural Number Simulation for Complex Systems ---

    Complex Reaction System Laboratory
    
    Copyright (c) 2022 Takashi Sato
    
    This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/



Description

This programs provide a natural number simulation to explore complex reaction systems. The numbers in this calculation means molecular numbers, cell numbers, living individual numbers, etc. This program contains time evolution algorithm code for calculating those natural numbers. You can use this program instead of conventional ordinary differencial equations(OEDs). OEDs can deal with phenomenon of vourious numerical systems. The Number Simulation also can solve those numerical reaction systems based on random natural number by binomial probability. This program enables non-stop calculation, and simple usage by input file writing. Enjoy this smart simulator.


Categories

 complex system, system biorogy, A-life, simulation 


File structuer

 This program uses seven python files and one json file as shown below.

    1. binomial_v015.py (main program)
        This is a main program. This contains reading process of a input file and 
        a main loop for calculation. 
    2. element_32.py
        The element class in this file defines elements in the input files. Elements
        are molecules or various cells or living individuals, and/or etc.
    3. reaction_49.py
        Classes in this file define several reactions for the elements in the input file.
    4. utility_48.py
         This program contains utilities for plotting process, file saving, time managing, and so on.
    5. setting_14.py
         This program contains utilities for input file setting.
    6. reactionManage_05.py  
           This file provides reaction process management codes.
    7. polymer_12.py
             Under constraction.
    8. binomial_parameters.json
           A json file which define calculation condition and result's setting.

              
 The program is developed by Spyder IDE 5.3.3 on Ubuntu 22.04.1 LT, 25 March 2023.

  

Getting started

  You can run your program by six dot(.)-py files above, a json file and one input file.
  The input file is writtn by plane text, which have .txt extension.
  The file should have four sections, *Time, *Element, *Reaction, and *Plot.
  Create one main project folder.
  Put six dot(.)-py files and the json file in a program-file holder which locate in the main holder.
  make an another holder in the master holder to put input files. (Look at "Folder structure.pdf")
      
  You need to change a input file name in the binomial_v015.py to run by Spyder.
  Running the binomial_v015.py, the calculation starts, and plots appeare in the plot window. 
  A test file below is inp_immune_323.txt. Below show explanation of four sections;
  *Time, *Element, *Reaction, and *Plot. The ** in below example means comment line. 
  Moreover, the json file is explained
   
    1. *Time
         You need to write start time, end time, 
         console-printout interval time, plot-out interval time, 
         csv-file output interval time, and the unit. 
         You can only write natural numbers. 
         The zero, 0 is available in the line. Calculations executes by every one interval.
           
         Format:
           *Time
            start time, end time, console out interval, plot out interval, csv-file out interval, time unit
         
         Example:
           *Time, 
           ** start, end, console out, plot out, csv out, time unit
                  0, 14400, 1440, 14400, 1440,  min

    2. *Element
         You write element items you want to simulate. 
         You can set the element name, initial number, color for plotting and marker for plotting. 
         Markers are available as follows for example.
           ["o", "v", "^", "<", ">","1", "2", "3", "4", "8",  \
           "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
         You can omit color and marker.
           
         Format:
           *Element
            element name, initial number, plot color, plot marker
               --- --- --- 
               --- --- --- 

         Example:
           *Element
           ** 0:element name, 1:initial number, 2:plot color, 3:plot marker
           virus, 500, Black, 8
           cell, 100000, Green, s
           virusCell, 0, p
           macrophage, 5000, 
           macrophageActive, 0,
           macrophageWithVirus, 0, 
           dendricCell, 2000, Blue,  
           dendricMHC, 0, Red,  
           naiveTh1, 10000, Green
           activeTh1, 0, 
           IFN, 0, Blue
           IL-12, 0

    3. *Reaction
         You define reactions for elements above. 
         Many reaction types are available as below. 
         Reaction multi; rM defines a reaction concerned with many kind of elements.  

              r1_0 : One kind of element decreases its number.
              r1_1 : One kind of element change to anothor kind of element. 
              r1_2 : One kind of element separate to two kind of element.
              r1_3 : One kind of element separate to three kind of element.
              r2_1 : Two kinds of element react, and change to one element.
              r2_2 : Two kinds of element react, and change to two kinds of element.
              r2_3 : Two kinds of element react, and change to three kinds of element.
              r3_1 : Three kinds of element react, and change to one kind of element.
              r3_2 : Three kinds of element react, and change to two kinds of element.
              r3_3 : Three kinds of element react, and change to three kinds of element.
              rM   : Some kinds of element react, and change to another some kinds element. 
              r1_+ : One kind of element increases its number by linear. 
              r1_- : One kind of element decreases its number by linear.    
        
         All reaction definition need reaction elements and created elements,
         and the reaction order for the elements. 
         For example, if one kind of element A becomes two kinds of elements: X and Y. 
         Below statement shows one A becomes two X and three Y. 
        
                   r1_2, 001, 1, A, 0.5, 2, X, 3, Y
        
         The first term is reaction type.
         the second is a name for identification.
         The third term and the forth one, “1, A” is reaction order and the element name.
         The fifth one, 0.5 is a reaction probability parameter.
         The sixth and the seventh, “1, X" is reaction order and a generated element name.
         The eigth and the nineth, “1, Y" is reaction order and an another generated element name.
       
         Reaction order have to be a natural number. 
         Element name have to be defined in *Element. 
       
         The rM allows many kinds of elements in before and after in the reaction definition.  
         Three-line statement defines one reaction. An example is shown below.
       
            rM,   002,  1, A, 10, B, 10, C, 2, D, 100, E
                         1000
                        1, X, 1, Y, 10, Z, 3, W  
                        
         where five kind of elements react, and create four kind of elements.
         The numbers before element name show reaction orders as like other reaction definitions. 
         The first line defines reacting elements. The third line defines as created elements. 
         You can describe many elements in line. The second line is the reaction probability parameter. 

         The *Reaction needs a global normalization parameter, if definitions of reactions contain r2_1, 
         r2_2, r2_3, r3_1, r3_2, r3_3, rM. 
         This parameter controls reaction probability through the algorithm.
       
         The reaction probability parameters and the global normalization parameter 
         can be real numbers. In the format as below, A, B, X, Y are element name
         defined in the *Element items. The pi stands for a probability parameter of each reaction. 

         Format:
          *Reaction, global normalization parameter
           r1_2, name, a, A, p1, x, X, y, Y
           r1_1, name, a, A, p2, x, X
           r1_0, name, a, A, p3
           r2_2, name, a, A, b, B, p4, x, X, y, Y
           r2_1, name, a, A, b, B, p5, x, X
           rM,   name, a, A, b, B, c, C, d, D, e, E, -------
                       p6
                       x, X, y, Y, z, Z, w, W, -------
           --- --- --- 
           --- --- --- 

         Example:
           *Reaction, 100000000
           r2_1, 001,  10, virus, 1, cell, 0.04, 1, virusCell
           r1_1, 002,   1, virusCell, 0.001, 100, virus
           r2_1, 003,   1, macrophage, 1, virus, 0.9, 1, macrophageWithVirus
           rM,   004,   1, macrophageWithVirus,  
                          0.9, 
                        1, macrophageWithVirus, 10, IFN, 10, IL-12
           r1_1, 005,   1, macrophageWithVirus, 0.1, 1, macrophage
           r2_1, 006,   1, virus, 1, dendricCell, 10, 1, dendricMHC
           rM,   007,   1, naiveTh1, 1, dendricMHC, 10, IFN, 10, IL-12
                        10000,
                        1, activeTh1, 1, dendricMHC
           r1_2, 013,   1, activeTh1, 1, 10, IFN, 1, activeTh1
           r2_1, 014,   1, macrophage, 2, IFN, 10, 1, macrophageActive 
           r2_1, 015,   1, macrophageActive, 10, virus, 1, 1, macrophageWithVirus
           r1_1, 018,   1, dendricMHC, 0.0002, 1, dendricCell
           r1_1, 019,   1, macrophageActive, 0.002, 1, macrophage
           r1_1, 020,   1, activeTh1, 0.001, 1, naiveTh1
           r1_0, 021,   1, IFN, 0.01
    
    4. *Plot 
         This section defines plotting condition. 
         Elements written in the same line are shown in one figure. 
         The plot-type is linear or log.
     
         Format:
          *Plot, plot-type
           A, X, Y
           B, W
           F
           --- --- --- 
           --- --- ---          
    
         Example:
           *Plot
           virus, virusCell, macrophageWithVirus
           cell, virusCell
           macrophage, macrophageActive, macrophageWithVirus
           dendricMHC, dendricCell
           IFN, IL-12
           activeTh1, naiveTh1
           
    5. binomial_parameters.json
          This file contains two definitions below.
          Defaults is all "YES".
             "EntropyCalc": "YES" or "NO": Entropy calculation cost is high at large numbers.
                                           If you don't need, should set "NO".
             "CSV_OUTPUT":"YES" or "NO":   Csv files contains all elements data at setting times.
                                           If you don't need csv files, set "NO". 
             "FIG_OUTPUT":"YES" or "NO":   Figuer's file type is png. 
                                           Figuers defined in *Plot are saved at setting times.  
                                           If you don't need plot graphs, set "NO".                                 
              
         
         
Executing a program

    Two excuting processes are abailable.
  You needs two holders in a master holder at least. One holder contains the six program files.
  The other holder should contains input text files like as mentioned above Getting started.  
  (Look at "Folder structure.pdf")
  
     1. Spyder
        
          One executing method use spyder in anaconda3. Open the main file, binomial_v015.py from Spyder. 
         You should write input file name in the appropriate line as follows,
         
              fName = 'inp_test_038.txt'
         
         "Run file" command in Spyder executes the input file. Results files will be put
          in a new holder which is created in the input file holder.
          
     2. command line
     
           Preparing holders are same as for 1.Spyder case.
           Open a terminal, and change directory to the program files　located directory.
           you write a command line in a terminal as follows.
           Executing a programExecuting a program
                  $ python binomial_v015.py inp_test_038.txt 
                  
              Return the line and the program starts.
              Result files will be located in a new created holder like as 1.spyder. 
       
             
Result file

    A result file holder is created in same holder of the input file. For example, 
  
  "inp_test_038_2023-3-25 13-46-12" for inp_test_038.txt.
  
  There are csv files and png files in it. Csv files are three types.
   
  inp_test_038_all.csv        :  Elements numbers at setting time in the row time.   
  inp_test_038_all_02.csv     :  Elements numbers at setting time in the column time.
  inp_test_038_information.csv:  Information of reaction(IR), accumulated IR, and reaction entropy 
                                 at setting time in the row time.
   
  Plotting figures of element number time series, which defined in input file, also are saved.  
