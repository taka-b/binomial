#!/bin/bash

# bash test_binomial_05.sh

echo test_binomial_05.sh

date

PROGRAM="binomial_189.py"
echo PROGRAM

python ${PROGRAM} inp_Glycolysis_90.txt
python ${PROGRAM} inp_polymer_183.txt
python ${PROGRAM} inp_oscillation_010.txt
python ${PROGRAM} inp_exponential_401.txt
python ${PROGRAM} inp_SIR_105.txt
python ${PROGRAM} Michaelis–Menten_005.txt
python ${PROGRAM} Set_membrane_108.txt
