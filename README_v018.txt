Binomial

-- Natural Number Simulation for Complex Systems --

    Complex Reaction System Laboratory

    Copyright (c) 2022- Takashi Sato
    
    This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/


0. Description

0.1. Overview:
  This program provides Natural Number Simulation (NNS) for analyzing complex reaction systems. 
  The numbers in this calculation represent quantities such as the number of molecules, cells, or living individuals, 
  with all numbers being natural numbers including zero. The program includes a time evolution algorithm to compute these natural numbers. 
  It can be used as a supplement to traditional Ordinary Differential Equations (ODE) or Petri nets. 
  NNS simulates chemical reaction systems and mathematical models through random natural number calculations based on binomial probabilities. 
  This program enables straightforward model definition through its non-halting calculation algorithm. 
　
0.2. Simulation:
　The program can simulate the time evolution of the "number" of molecules in reaction systems such as:
　
  lA + mB + nC　+ - - -   → 　sX + tY + uZ + - - - 
　
  Here,A,B,C,X,Y,and Z are reaction components, andl,m,n,s,t, and u are coefficients representing the stoichiometric quantities of the reactions. 
  While details are provided in Section 8, Reference [2], the program can compute time evolution equations for any number of elements 
  and stoichiometric quantities simultaneously for any number of stoichiometric equations.


0.3. Categories:
  Complex Systems, Systems Biology, Bioinformatics, A-life, Simulation
 

1. File Structure

  This program consists of nine Python files and one JSON file. 
  These files are collectively referred to as program files. 
  Additionally, one input file is required to run the program.

  1.1. binomial_v018_02.py (Main Program)
    This is the main code that includes the process of reading the input file and executing calculations.

  1.2. binomial_parameters_11.json
    This file contains parameters that determine the conditions for the calculations and the settings for the results.

  1.3. element_43.py
    This code defines the calculation elements. Element objects are created based on the element names and 
    initial quantities defined in the *Element section of the input file.

  1.4. reaction_83.py
    This code is used to calculate the reaction equations. 
    The reaction equations are defined in the *Reaction section of the input file.

  1.5. utility_75.py
    This file contains utility-related code for outputting result graphs and CSV files.

  1.6. setting_39.py
    This code is related to reading the input file.

  1.7. utility_functions.py
    This file contains functions necessary for the settings.

  1.8. polymer_13.py
    Under construction.

  1.9. reactionManage_07.py
    Under construction.

  1.10. setManage_04.py
    Under construction.

  These codes were developed using Spyder IDE 5.4.3 on Ubuntu 22.04.2 LTS as of Junuary 2025. 
  They are compatible with both Windows and Linux (some input files are Linux-only).
 
2. Folder Preparation

  Create a single main folder. Inside this main folder, create a folder for the program and 
  store the aforementioned program files in it. Additionally, create another folder within the main folder for input files, 
  and store your input files there (refer to Figure 1 in Readme_v018_Figuers.pdf). 
  You may create as many input-file folders as you wish, but please ensure not to create multiple input files with the same name.
　　

3. Input File Structure 1

  This program can be executed by preparing the program files mentioned above along with a single input file. 
  The input file should be a plain text file with a .txt extension and should include four sections: *Time, *Element, *Reaction, and *Plot. 
  The description below pertains to the test file inp_immune_323.txt. 
  Here, we provide explanations for the four sections: *Time, *Element, *Reaction, and *Plot. 
  Note that in all cases below, ** and # indicate comment lines.

   
3.1. *Time

  Here, you should write the start and end times, as well as set the intervals for console output, plot output, CSV file output, 
  and specify the unit. Only natural numbers, including 0, are available for these values. Calculations are executed at each unit interval. 
  In the example provided, calculations are executed one by one from 0 to 14400. 
  Intermediate results are output to the console every 1440 units, plots are displayed every 7200 units, 
  and values of elements are output to a file every 1400 units. The unit in this case is "min", 
  but please pay attention to the relationship with the rate constant, as it is specified by the user. 

         Format:
           *Time
            start time, end time, console out interval, plot out interval, csv-file out interval, time unit
         
         Example:
           *Time, 
           ** start, end, console out interval, plot out interval, CSV time interval, time unit
           0, 14400, 1440, 7200, 1440,  min

3.2 *Element

  This section is for describing the elements you want to simulate. 4
  At a minimum, you need to specify the element's name and its initial count. 
  Ensure that element names are unique and do not overlap. Additionally, as shown in the example below, 
  the initial count of the elements must be set as a natural number, including 0. 
  However, exponential notation, such as 1e5 or 1.1e4, is also acceptable.
  Additionally, you can set the color and marker for plotting. If you do not specify a color or marker, 
  arbitrary ones will be assigned. For colors, you can set values such as 

         ['Black', 'Green', 'Yellow', 'Gray', 'Blue', 'Red', 'Orange'], or any color from matplotlib.colors.cnames.

  For markers, you can set values from the following options:

         ["o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"].
            
          
         Format:
           *Element
            element name, initial number, plot color, plot marker
               --- --- --- 
               --- --- --- 

         Example:
           *Element
           ** 0:element name, 1:initial number, 2:plot color
           virus,               500, Black, 8
           cell,                1e5, Green, s
           virusCell,             0, p
           macrophage,         5000, 
           macrophageActive,      0,
           macrophageWithVirus,   0, 
           dendricCell,        2000, Blue,  
           dendricMHC,            0, Red,  
           naiveTh1,          1.1e4, Green
           activeTh1,             0, 
           IFN,                   0, Blue
           IL-12,                 0
          
3.3. *Reaction

  This section defines the reactions between the elements mentioned above, or reactions involving individual elements. 
  Various types of reactions are available for use, as shown below. 
  Reaction Multi (rM) allows for the definition of reactions involving a variety of element types.
 
          r1_0: A certain percentage decrease of one type of element
          r1_1: One type of element transforms into another single element
          r1_2: One type of element transforms into two different types of elements
          r1_3: One type of element transforms into three different types of elements
          r2_1: Two types of elements transform into one different element
          r2_2: Two types of elements transform into two different types of elements
          r2_3: Two types of elements transform into three different types of elements
          r3_1: Three types of elements transform into one different element
          r3_2: Three types of elements transform into two different types of elements
          r3_3: Three types of elements transform into three different types of elements
          rM:   A variety of elements transform into another variety of elements
          r1_+ : The count of one type of element increases linearly
                   Example）　r1_+, 300, 0, 0, 1, 5, S1　   (test_059.txt)
          r1_- : The count of one type of element decreases linearly
                   Example）　r1_-, 400, 1000, D, 100, 0, 0    (test_059.txt)
          r+-= : The element to the left of the "=" is used to calculate the sum of the multiplication of the coefficient and the number of elements,
                 and the result is assigned to the element to the right (used for verification, etc.).
                   例）　r+-=, 100, 1, N, 1, P, =, 1, NP         
 
  For reaction definitions, you typically need information about the reactant and product elements, 
  their stoichiometric coefficients, and the numeric setting of the rate constant. 
  For reactions r1_1 and above (from r1_1 to rM as mentioned above), 
  the reactant and product elements can include the same elements. Here’s how to describe them:

  For example, in reaction r1_2, one type of element A transforms into two different types of elements X and Y. 
  If we assume that one A turns into two X’s and three Y’s, the definition would look like this: 
 
          r1_2, 001, 1, A, 0.5, 2, X, 3, Y
 
  The first term defines the reaction type. 
  The second is an identifier; together with the first term, they create a unique reaction name like "r1_2_001", 
  so ensure there are no duplicates. The third and fourth terms "1, A" specify the stoichiometric coefficient and 
  the reactant element name. The fifth term, 0.5, is the rate constant. 
  The sixth and seventh terms "2, X" and the eighth and ninth terms "3, Y" specify the stoichiometric coefficients and 
  the names of the product elements.
  Stoichiometric coefficients must be natural numbers. The element names must be defined in the *Element section. 
  The probability parameter can be a decimal or a natural number.
       
  The "rM" allows for the definition of reactions with multiple element types before and after the reaction. 
  For example, a reaction can be defined using three lines like this:
 
          rM,   002,  1, A, 10, B, 10, C, 2, D, 100, E
                      1000
                      1, X, 1, Y, 10, Z, 3, W
                       
  This defines a reaction where five types of elements react to produce four types of elements. 
  The numbers before the element names are the stoichiometric coefficients, similar to other reactions. 
  The first line defines the reactant elements, the second line is the rate constant, 
  and the third line defines the product elements. This way, many elements can be described in a line, 
  with virtually no limitations.
  In the *Reaction definition, a normalization parameter is required on the same line. 
  Ideally, this value should be around the same magnitude as the total number of elements in the reaction system, 
  but there are no strict limitations. A larger value results in a smaller probability of the reaction occurring, 
  while a smaller value increases the probability. Reactions like r2_1, r2_2, r2_3, r3_1, r3_2, r3_3, and 
  rM are influenced by the normalization parameter through the algorithm, 
  in conjunction with the rate constant.
  ("Application of a Novel Numerical Simulation to Biochemical Reaction Systems" by Takashi Sato, doi: 
  https://doi.org/10.1101/2023.08.10.552732)
  Both the rate constant and the normalization parameter can be decimals. 
  In the format below, A, B, X, and Y are element names defined in the *Element section, and pi (p1, p2, etc.) represents 
  the rate constants for each reaction.

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

3.4. *Plot
　　　　
 In this section, you define the plotting conditions. 
 Elements written on the same line will be displayed in a single graph. 
 The type of vertical axis for the plot can be either linear or logarithmic. 
 If not specified, it will be displayed as "linear" by default.
 This allows you to visually organize and analyze the results of your simulation, 
 ensuring that all necessary elements are displayed together and in the appropriate format.  

         Format:
          *Plot, plot-type (linear or log)
          ** second item is "linear" or "log".
           A, X, Y
           B, W
           F
           --- --- --- 
           --- --- ---          
    
        Example:
         *Plot, log
           virus, virusCell, macrophageWithVirus
           cell, virusCell
           macrophage, macrophageActive, macrophageWithVirus
           dendricMHC, dendricCell
           IFN, IL-12
           activeTh1, naiveTh1
           
3.5. binomial_parameter_06.json

  In this file, you set parameters for CSV file output and figure generation. 
  For "YES" or "NO" options, please select one. For file outputs, if "YES" is selected, 
  values will be output at the intervals specified in the *Time section of the input file. 
  If "NO" is selected, no files will be generated.

    "making_folder":    ["YES" or "NO"],If you do not want to create a folder for output results, please select "NO."  
                                        In this case, result files will not be created regardless of selecting "YES" for the output results below.

    "InformationCalc": ["YES" or "NO"], Calculates the amount of information and its cumulative value, and outputs it to a CSV file.
                                        (For detailed definitions, refer to section 8 in the literature [2])
                                        The file name will be [input file name]_information.csv.
        
    "EntropyCalc":     ["YES" or "NO"], Calculates entropy and outputs it to a CSV file.
                                       (For detailed definitions, refer to section 8 in the literature [2])
                                       The file name will be [input file name]_entropy.csv.
                                       Calculating entropy can be computationally intensive for large numbers, so switch as needed.
        
    "n_p_Binomial":    ["YES" or "NO"], Outputs n and p used in np.random.binomial(n, p).
                                        (For detailed definitions, refer to section 8 in the literature [2])
                                        The file name will be [input file name]_probability.csv.
                              
    "CSV_OUTPUT":      ["YES" or "NO"], If set to "NO", none of the CSV files will be output.    
                                        Select "YES" if you want to output at least one CSV file.
       
    "FIG_OUTPUT":      ["YES" or "NO"], If "YES" is selected, the plots defined in *Plot will be output at intervals specified by the plot out interval in *Time.
                                        The file type for the plots is png.
                                        Select "NO" if you do not want to output plots.

    "Fig_from_CSV":    ["YES" or "NO"], If "YES" is selected, plots will be created at intervals set by the csv-file out interval in *Time.
                                                If "NO" is selected, plots will be created using data from every step.
                                                Selecting "YES" is recommended when there are many calculation steps.
     
    "RestartFile":     ["YES" or "NO"], A restart file will be created using the final values of the elements calculated from the input file as initial values.
                                        For example, for test_059.txt, a file named test_059_Re.txt will be created in the same folder as the input file.
                                        You can use this restart file name to resume calculations.

    "RestartFile_period":    [integer], Not set

    "Matplotlib(1) or Seaborn(2)": [1 or 2], Select 1 for output using Matplotlib, or 2 for output using Seaborn.
                                             Matplotlib uses markers, whereas Seaborn does not.

    "Seaborn linewidth": [0.1 < decimal < 10], The line width setting for Seaborn. Values between 0.1 and 10 are recommended.
        
    "Optimization":     ["YES" or "NO"], For now, please select "NO."

    "Reaction_Order":   [ 'ordered' or 'random'], Calculation order for a reaction set



4. Input File Structure 2 (Optional Settings) (e.g., test_059.txt)

4.1. *ElementInOut

The *ElementInOut setting is available to represent the inflow and outflow of elements in the computational domain.  
This allows the representation of element inflow and outflow during the calculation process.

    Format:    
      *ElementInOut
      element name, initial number, plot color, marker, <brank>, type-0, at time, amaunt, at time, amaunt, -> -> 
      element name, initial number, plot color, marker, <brank>, type-1, interval, amaunt
      element name, initial number, plot color, marker, <brank>, type-2, const, amplitude, period-time, add-interval
           --- --- --- 
           --- --- ---   
        
    Example:
     *ElementInOut
      Q,      270, blue, s, ,    type-0, 10, 300, 40, 100, 50, 50, 60, 500, 70, 500
      T-in,     0, blue, h, ,    type-1, 2, 1e2
      T-out,  1e5, magenta, 4, , type-1, 2, -5e2
      B,        0,  purple, 2, , type-2, 100, 10, 10,  50


5. Input File Structure 3 (Optional Settings) (e.g., Set_405.txt)

  This section describes the method for formulating the exchange of molecules and reactions 
  within cells and intracellular organelles using the concept of sets. 
  Previously, a single system was implicitly assumed. Using *ElementInOut, you could define substances flowing into and out of the system, 
  but all molecules and reactions defined by *Element and *Reaction were considered to be within a single system. 
  Here, we show how to define one or more compartmental regions (with definable substance exchange) within that system.

  First, define one or more compartmental regions within the system using *Set_01. 
  Then, using *Set_02, define multiple regions within each of the *Set_01 defined regions.
  Figure 2 is a conceptual diagram of the defined regions. The outermost region is defined by the previous definition files, 
  within which the regions defined by *Set_01 exist, and further inside, the regions defined by *Set_02 are present. 
  It is also possible to define multiple *Set_01 and *Set_02 regions, as shown in Figure 3.

  As shown below, each hierarchical level requires one or more input files. These files are combined to create a new input file, 
  which is eventually read to start the calculations.

5.1. *Set_01
  
  To define the first-level region, add the following lines to the input file.

    Format:    
      *Set_01
       set name, file name, number of the set

    Example:
      *Set_01
      C1, Set01_401.txt, 1

  This defines one region named C1 in the global region. 
  In the file Set01_401.txt, you can define *Element, *Reaction, and *Plot as usual. 
  However, to distinguish them from the global region, you should generally append ":=" after the element names and reaction-specific names. 
  Therefore, it is standard to include ":=" after the element names in the *Plot definitions as well.

5.2. *Set_02

  To define the second-level region, add the following lines to the input file.

    Format:    
      *Set_02
       set name, upper set name (in *Set_01), upper set number(in *Set_01), file name, number of the set

    Example:
      *Set_02
      M1, C1, 1, Set02_401.txt, 1

  This defines a region named M1 within the region C1 defined by *Set_01. 
  In the file Set02_401.txt, you can define *Element, *Reaction, and *Plot as usual. 
  However, to distinguish them from the global region and the regions defined by *Set_01, 
  you should generally append "::" after the element names and reaction-specific names. 
  Therefore, it is standard to include "::" after the element names in the *Plot definitions as well.

5.3. Examples of Each File

  An example is shown in Figure 4. The global region file is named Set_401.txt. 
  Below is an example where there is one Set_01 region within the global region, and within that, there is one Set_02 region. 
  The definition of the Set_01 region is written in Set_401.txt, and the definition of the Set_02 region is written in Set02_401.txt. 
  Set_401.txt serves as the master file, and when this file is read, the remaining two files are also read and combined to create a new input file, 
  Set_401_new.txt.

  Figure 4 illustrates the elements within each region. 
  Although it may appear that there is no exchange of elements between regions in this diagram, 
  it is possible to define the exchange of substances using membrane proteins, as described below. 
  Diffusion can also be defined for movement. These definitions of substance movement are explained in detail in sections 5.3.2 and 5.3.3.

  Please note that a and a:= in Figure 4 represent the same substance, but the name changes due to the movement between regions. 
  Figure 5 schematically shows the movement reactions of each element in the following files.

5.3.1. Set_401.txt
   
  Two nested regions are defined using *Set_01 and *Set_02.

      *Time,     
       0,  10000,   1000,   5000,    100,    msec

      *Element
       H2O, 1e13, aqua, 4
       OH-,  1e5, turquoise, 2
       H+,   1e5, pink, 3
       a,    1e6, Blue, 4
       b,    1e5, DarkTurquoise, 2
       c,    1e4, DeepPink, 3
       r,      0, green, 4

      *Reaction, 1e13
       r1_2, 000, 1, H2O,        1e-10, 1, H+, 1, OH-
       r2_1, 001, 1, H+, 1, OH-,   1e4, 1, H2O

      *Set_01
       C1, Set01_401.txt, 1

      *Set_02
       M1, C1, 1, Set02_401.txt, 1

      *Plot, log
       a, b, c, r

5.3.2. Set01_401.txt
   
  Elements, reactions, and plots within Set_01 are defined, with ":=" appended to their names. 
  Membrane protein elements like mem_P1:= and mem_P2:= are defined, 
  and elements like a and b are taken from the global region and renamed a:= and b:=.

  Additionally, reaction 110:= is a reaction within Set_01 that uses ATP:= to incorporate b from outside the region. 
  This allows for simulations where the overall number of elements like a and b is conserved even as they move between regions.
  Furthermore, mem_P6:= is a membrane protein model that transports r:= from within the region to outside the region. 
  The diffusion of molecules commonly seen in small molecules can also be modeled. 
  Reaction 120:= is an example of this, defining the simple diffusion of c from the global region into Set_01. 
  Conversely, reverse diffusion is defined by reaction 121:=.

      *Element
       H2O:=, 1e10, aqua, 4
       OH-:=,  1e2, turquoise, 2
       H+:=,   1e2, pink, 3
       a:=,      0, Blue, 4
       b:=,      0, DarkTurquoise, 2
       c:=,      0, DeepPink, 3
       en_X:=, 3e3, darkkhaki, 3
       en_Z:=, 2e3, BlueViolet, _
       l:=,      0, MediumOrchid, >
       m:=,    1e5, indigo, d
       n:=,      0, tomato,  *
       q:=,      0, red, 3
       r:=,      0, green, 4
       ATP:=,  1e7, green, 4
       ADP:=,  1e7, LightPink, |
       Pi:=,   1e7, BlueViolet, _
       mem_P1:=, 1e3, chocolate, +
       mem_P2:=, 5e2, greenyellow, o
       mem_P6:=, 3e2, darkmagenta, x

      *Reaction, 1e10
       r1_2, 000:=, 1, H2O:=,            1e-10, 1, H+:=, 1, OH-:=
       r2_1, 001:=, 1, H+:=, 1, OH-:=,     1e4, 1, H2O:=
       r2_2, 100:=, 1, a,    1, mem_P1:=,  1e2, 1, a:=, 1, mem_P1:=
       rM,   110:=, 1, b, 1, mem_P2:=, 1, ATP:=, 1, H2O:=
                    1e6
                    1, b:=, 1, mem_P2:=, 1, ADP:=, 1, Pi:=
       r1_1, 120:=, 1, c,   0.5, 1, c:=
       r1_1, 121:=, 1, c:=, 0.1, 1, c
       r3_2, 130:=, 1, a:=, 1, b:=, 1, en_X:=, 1e8, 1, l:=, 1, en_X:=
       r3_2, 140:=, 1, c:=, 1, q:=, 1, en_Z:=, 1e6, 1, r:=, 1, en_Z:=
       r2_2, 150:=, 1, r:=, 1, mem_P6:=,       1e4, 1, r, 1, mem_P6:=

      *Plot, log
       a:=, b:=, c:=
       l:=, m:=, q:=, r:=

      *Plot
       en_X:=, en_Z:=, mem_P1:=, mem_P2:=, mem_P6:=  

5.3.3. Set02_401.txt

  Elements, reactions, and plots within Set_02 are defined, with "::" appended to their names. 
  Here, mem_P3:: is defined as a membrane protein element and acts as a co-transporter in reaction 100::, 
  taking in l:= from the Set_01 region and expelling n:: from Set_02 to Set_01.
  Additionally, mem_P4:: is another membrane protein element that takes in m:= from the Set_01 region. 
  As a result, elements from outside the region, such as l:= and m:=, are brought into the region and renamed to l:: and m::, respectively. 
  Consequently, n:: that was in Set_02 is renamed to n:=.
  Furthermore, mem_P5:: is a membrane protein element that transports q:: from inside the region to outside. 
  Reaction 130:: involves consuming ATP within the region to transport q::.

      *Element
       H2O::, 1e9, aqua, 4
       OH-::, 1e2, turquoise, 2
       H+::,  1e2, pink, 3
       l::,     0, MediumOrchid, >
       m::,     0, indigo, d
       n::,   1e5, tomato,  *
       q::,     0, red, 3
       en_Y::,1e4, MediumOrchid, +
       ATP::, 1e6, green, 4
       ADP::, 1e6, LightPink, |
       Pi::,  1e6, BlueViolet, _
       mem_P3::, 5e3, darkmagenta, x
       mem_P4::, 3e3, gray,   +
       mem_P5::, 2e3, salmon, H

      *Reaction, 1e9
       r1_2, 000::, 1, H2O::,          1e-10, 1, H+::, 1, OH-::
       r2_1, 001::, 1, H+::, 1, OH-::,   1e4, 1, H2O::
       r3_3, 100::, 1, l:=, 1, n::, 1, mem_P3::, 1e2, 1, l::, 1, n:=, 1, mem_P3::
       r2_2, 110::, 1, m:=, 1, mem_P4::,         1e3, 1, m::, 1, mem_P4::
       rM,   120::, 1, l::, 1, m::, 1, n::, 1, en_Y::
                    1e6
                    1, q::, 1, en_Y::
       rM,   130::, 1, q::, 1, mem_P5::, 1, ATP::, 1, H2O::
                    1e4
                    1, q:=, 1, mem_P5::, 1, ADP::, 1, Pi::

      *Plot, log
       l::, m::, n::, q::

      *Plot
       en_Y::, mem_P3::, mem_P4::, mem_P5::

5.3.4. Composite input file (Set_401_new.txt)

  When the input file for the global region is read, the files for each region are also read, 
  and a composite file is created. For example, for Set_401.txt, a file named Set_401_new.txt is generated. 
  Elements and reactions within each calculation region are named with the region's name appended after ":=" or "::", such as C1_1 or C1_1::M1_1. 
  The _1 in C1_1 or C1_1::M1_1 is a numbering system used to distinguish between multiple regions, 
  such as C1_2 or C1_2::M1_1, as explained below (5.3.5).
  In this way, the renaming of element and reaction names allows for the calculation of reactions within each region. 
  Below is an excerpt from Set_401_new.txt.


      ** ************************************ 
      *SetDefine, C1_1
      ** ************************************ 
      # 2024.3.20 Takashi Sato

      *Element
       H2O:=C1_1,  1e10,  aqua,  4
       OH-:=C1_1,   1e2,  turquoise,  2
       H+:=C1_1,    1e2,  pink,  3
       a:=C1_1,       0,  Blue,  4
       b:=C1_1,       0,  DarkTurquoise,  2
       c:=C1_1,       0,  DeepPink,  3

       en_X:=C1_1,  3e3,  darkkhaki,  3
       en_Z:=C1_1,  2e3,  BlueViolet,  _

       l:=C1_1,       0,  MediumOrchid,  >
       m:=C1_1,     1e5,  indigo,  d
       n:=C1_1,       0,  tomato,   *
       q:=C1_1,       0,  red,  3
       r:=C1_1,       0,  green,  4

       ATP:=C1_1,   1e7,  green,  4
       ADP:=C1_1,   1e7,  LightPink,  |
       Pi:=C1_1,    1e7,  BlueViolet,  _

       mem_P1:=C1_1,  1e3,  chocolate,  +
       mem_P2:=C1_1,  5e2,  greenyellow,  o
       mem_P6:=C1_1,  3e2,  darkmagenta,  x

      *Reaction,  1e10
       r1_2,  000:=C1_1,  1,  H2O:=C1_1,           1e-10,  1,  H+:=C1_1,  1,  OH-:=C1_1
       r2_1,  001:=C1_1,  1,  H+:=C1_1,  1,  OH-:=C1_1,    1e4,  1,  H2O:=C1_1
       
       r2_2,  100:=C1_1,  1,  a,    1,  mem_P1:=C1_1,  1e2,  1,  a:=C1_1,  1,  mem_P1:=C1_1
       
       rM,    110:=C1_1,  1,  b,    1,  mem_P2:=C1_1,  1,  ATP:=C1_1,  1,  H2O:=C1_1
                          1e6
                          1,  b:=C1_1,  1,  mem_P2:=C1_1,  1,  ADP:=C1_1,  1,  Pi:=C1_1

       r1_1,  120:=C1_1,  1,  c,  0.1,  1,  c:=C1_1
       r1_1,  121:=C1_1,  1,  c:=C1_1,  0.1,  1,  c
       r3_2,  130:=C1_1,  1,  a:=C1_1,  1,  b:=C1_1,  1,  en_X:=C1_1,  1e8,  1,  l:=C1_1,  1,  en_X:=C1_1
       r3_2,  140:=C1_1,  1,  c:=C1_1,  1,  q:=C1_1,  1,  en_Z:=C1_1,  1e6,  1,  r:=C1_1,  1,  en_Z:=C1_1

       r2_2,  150:=C1_1,  1,  r:=C1_1,  1,  mem_P6:=C1_1,  1e4,  1,  r,  1,  mem_P6:=C1_1

      *Plot,  log
       a:=C1_1,  b:=C1_1,  c:=C1_1
       l:=C1_1,  m:=C1_1,  q:=C1_1,  r:=C1_1

      *Plot
      en_X:=C1_1,  en_Z:=C1_1,  mem_P1:=C1_1,  mem_P2:=C1_1,  mem_P6:=C1_1

      ** ************************************ 
      *SetDefine, C1_1::M1_1
      ** ************************************ 
      # 2024.3.20 Takashi Sato

      *Element
       H2O::C1_1::M1_1,  1e9,  aqua,  4
       OH-::C1_1::M1_1,  1e2,  turquoise,  2
       H+::C1_1::M1_1,   1e2,  pink,  3

       l::C1_1::M1_1,      0,  MediumOrchid,  >
       m::C1_1::M1_1,      0,  indigo,  d
       n::C1_1::M1_1,    1e5,  tomato,   *
       q::C1_1::M1_1,      0,  red,  3

       en_Y::C1_1::M1_1, 1e4,  MediumOrchid,  +

       ATP::C1_1::M1_1,  1e6,  green,  4
       ADP::C1_1::M1_1,  1e6,  LightPink,  |
       Pi::C1_1::M1_1,   1e6,  BlueViolet,  _

       mem_P3::C1_1::M1_1,  5e3,  darkmagenta,  x
       mem_P4::C1_1::M1_1,  3e3,  gray,    +
       mem_P5::C1_1::M1_1,  2e3,  salmon,  H

      *Reaction,  1e9
       r1_2,  000::C1_1::M1_1,  1,  H2O::C1_1::M1_1,           1e-10,  1,  H+::C1_1::M1_1,  1,  OH-::C1_1::M1_1
       r2_1,  001::C1_1::M1_1,  1,  H+::C1_1::M1_1,  1,  OH-::C1_1::M1_1,    1e4,  1,  H2O::C1_1::M1_1

       r3_3,  100::C1_1::M1_1,  1,  l:=C1_1,  1,  n::C1_1::M1_1,  1,  mem_P3::C1_1::M1_1,  1e2,  1,  l::C1_1::M1_1,  1,  n:=C1_1,  1,  mem_P3::C1_1::M1_1
       r2_2,  110::C1_1::M1_1,  1,  m:=C1_1,  1,  mem_P4::C1_1::M1_1, 1e3,  1,  m::C1_1::M1_1,  1,  mem_P4::C1_1::M1_1

       rM,    120::C1_1::M1_1,  1,  l::C1_1::M1_1,  1,  m::C1_1::M1_1,  1,  n::C1_1::M1_1,  1,  en_Y::C1_1::M1_1
                                1e6
                                1,  q::C1_1::M1_1,  1,  en_Y::C1_1::M1_1

       rM,    130::C1_1::M1_1,  1,  q::C1_1::M1_1,  1,  mem_P5::C1_1::M1_1,  1,  ATP::C1_1::M1_1,  1,  H2O::C1_1::M1_1
                                1e4
                                1,  q:=C1_1,  1,  mem_P5::C1_1::M1_1,  1,  ADP::C1_1::M1_1,  1,  Pi::C1_1::M1_1

      *Plot,  log
       l::C1_1::M1_1,  m::C1_1::M1_1,  n::C1_1::M1_1,  q::C1_1::M1_1

      *Plot
       en_Y::C1_1::M1_1,  mem_P3::C1_1::M1_1,  mem_P4::C1_1::M1_1,  mem_P5::C1_1::M1_1


5.3.5. When Multiple Regions Exist (Set_402.txt)

  Here, we explain the case where multiple regions exist within the global region. 
  The Set_402.txt file shown below is an example where there are two types of regions, with two and three of each type within Set_01, 
  and within Set_02, each Set_01 region contains different Set_02 regions, with two and one of each respectively.
  When this input file is read, five Set_01 regions are created within the global region. 
  Each C1 region contains two M1 regions, and each C2 region contains one M2 region. 
  This is illustrated in Figure 6. Including the global region, there are a total of 13 regions.
  The elements and reaction names in each region are distinguished and calculated by appending the region names, 
  such as C2_3::M2_1, to the end of their names. Below is the content of Set_402.txt.

      *Time,     
       0,  10000,   1000,   5000,    100,    msec

      *Element
       H2O, 1e13, aqua, 4
       OH-,  1e5, turquoise, 2
       H+,   1e5, pink, 3
       a,    1e6, Blue, 4
       b,    1e5, DarkTurquoise, 2
       c,    1e4, DeepPink, 3
       r,      0, green, 4

      *Reaction, 1e13
       r1_2, 000, 1, H2O,        1e-10, 1, H+, 1, OH-
       r2_1, 001, 1, H+, 1, OH-,   1e4, 1, H2O

      *Set_01
       C1, Set01_402_01.txt, 2
       C2, Set01_402_02.txt, 3

      *Set_02
       M1, C1, 2, Set02_402_01.txt, 2
       M2, C2, 3, Set02_402_02.txt, 1

      *Plot, log
       a, b, c, r

  Additionally, it is possible to define *Set_02 as follows, while keeping the definition of *Set_01 unchanged (Set_403.txt). 
  In this case, each C1 region contains two M1 regions and one M2 region.
　
      *Set_02
       M1, C1, 2, Set02_402_01.txt, 2
       M2, C1, 2, Set02_402_02.txt, 1
       M2, C2, 3, Set02_402_02.txt, 1

  Furthermore, the following definition is also possible. 
  In this case, two M1 regions are created within one of the C2 regions (Set_404.txt)

      *Set_02
       M1, C1, 2, Set02_402_01.txt, 2
       M2, C1, 2, Set02_402_02.txt, 1
       M1, C2, 1, Set02_402_01.txt, 2
       M2, C2, 3, Set02_402_02.txt, 1   


6. Running the Program

  Two execution processes are available. 
  One is running the program directly from Spyder, and the other is running it from the command line.

6.1. Spyder
        
  One way to run the program is to use Spyder with Anaconda3. Open the main program file binomial_v017.py in Spyder. 
  Enter the input file name on the appropriate line as follows. 
  Since fName is already specified in the main program, replace it with your desired file name.         
               
      input_file ="inp_immune_323.txt"
         
  Execute the calculation using Spyder's "Run File" command. 
  Result files will be placed in a newly created folder within the folder containing the input file.
          
6.2. Command Line / Terminal

  The folder preparation is the same as in the Spyder case. 
  Open a terminal (e.g., Anaconda Powershell Prompt) and change the directory to the one containing the program file. 
  Enter the following command in the terminal:           

      > python binomial_v018_02.py inp_immune_323.txt
                  
  Press Enter to start the program. Result files will be placed in a newly created folder, similar to the Spyder case.


7. Result Files

  The result files folder is created in the same directory as the input file. For example:

  When running the previous "inp_immune_323.txt", a folder named "inp_immune_323_yyyy-mm-dd hh-mm-ss" is created, containing the result files.

  This folder contains time-series plots (PNG files) of the element counts defined in the input file. 
  Additionally, CSV files are saved. There are three types of CSV files:

    inp_immune_323_all.csv: Records the element counts at the specified times, with each row representing a time point.
    inp_immune_323_all_02.csv: Records the element counts at the specified times, with each column representing a time point.
    inp_immune_323_information.csv: Provides information on instantaneous reaction (IR), cumulative IR, and reaction entropy, 
                                    recorded at the specified times, with each row representing a time point.
    inp_immune_323_probability.csv：It outputs the variables "n" and "p" provided to `random.binomial(n, p)`, which returns random integers.


8. literature

[1] bioRxiv:「Application of a Novel Numerical Simulation to Biochemical Reaction systems」
　　 Takashi Sato, doi: https://doi.org/10.1101/2023.08.10.552732

[2] Front. Cell Dev. Biol., 06 September 2024
    Sec. Cellular Biochemistry
    Volume 12 - 2024 | https://doi.org/10.3389/fcell.2024.1351974

 
 
