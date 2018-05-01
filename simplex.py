import numpy as np
import scipy
import sys
import fractions
import json
import pl


#Define o tipo de simplex a ser aplicado
def tipo_sol(progL):
    if(all(i > 0 for i in progL.FPI_b)):
        if(all(i > 0 for i in progL.FPI_c)):
            print("Case B & C positives\n")
            return 42
        else:
            print("Case Primal\n")
            return 1
    else:
        if(all(i > 0 for i in progL.FPI_c)):
            print("Case Dual")
            return 2
        else:
            print("Case Primal, with b also negative")
            for x in range(len(progL.FPI_b)):
                progL.multiply_line(x, -1)
            return 1

TODO:

pivoteamentos, simplex dual e primal, simplex primal com auxiliar, respostas
checar ilimitada, checar inviável

#def pivo_primal(progL):








#c = [1,1,1]

#if(all(i > 0 for i in c)):
    print(c)
