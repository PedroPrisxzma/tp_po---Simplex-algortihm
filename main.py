import numpy as np
import scipy
import sys
import fractions
import json
import pl
import simplex

#Found at https://stackoverflow.com/questions/42209365/numpy-convert-decimals-to-fractions
#Changes decimals into fractions on numpy arrays
np.set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})

name = sys.argv[1]
file = open(name, "r")
m = file.readline()
n = file.readline()
hue = file.readline()

input_pl = np.array(json.loads(hue), dtype=float)

#Separate A e b
K = pl.split_b(input_pl)

#constructs matrix A, in a numpy array format, separating from c vector
Amatrix =  np.array([l.tolist() for l in K[0][1:]])

#PL contruction
progL = pl.PL(Amatrix, K[0][0], K[1][1:], int(n), int(m))
#puts it in FPI format
progL.make_FPI()

#pl.print_test(progL)

a = simplex.tipo_sol(progL)

