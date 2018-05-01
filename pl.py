import numpy as np
import scipy
import sys
import fractions
import json
import pl

#The Programação Linear class
class PL:
   #Pl, constructor
   def __init__(self, A, c, b, n, m):

       self.A = A #matrix A
       self.c = c #vector c
       self.b = b #vector b

       #matrix A dimensions
       self.n = n #columns
       self.m = m #lines

       #FPI elements for the tableu
       self.FPI_A = 0
       self.FPI_b = 0
       self.FPI_c = 0
       self.FPI_y = 0
       self.FPI_op_matrix = 0


   #Default prints
   def displayA(self):
       print("Matrix A\n",self.A)

   def displayc(self):
       print("Vector c\n",self.c)

   def displayb(self):
       print("Vector b\n",self.b)

   def displayDimensoes(self):
       print("linhas:",self.m,"colunas:", self.n)

   #Format FPI para o tableu
   def make_FPI(self):
       #Faz matriz A da FPI
       self.FPI_A = np.zeros((self.m, self.n + self.m))
       self.FPI_A[:,:-self.m] = self.A
       self.FPI_A[:,self.n:] = np.identity(self.m)

       #Faz o vetor c
       self.FPI_c = np.zeros(self.n + self.m)
       self.FPI_c[:-self.m] = self.c * (-1)

       self.FPI_op_matrix = np.identity(self.m)
       self.FPI_y = [0 for x in range(self.m)]
       self.FPI_b = self.b

   def display_FPI(self):
       print("FPI A\n", self.FPI_A)
       print("FPI b\n", self.FPI_b)
       print("FPI c\n", self.FPI_c)
       print("FPI y\n", self.FPI_y)
       print("FPI Op\n", self.FPI_op_matrix)

   #operações na PL
   def multiply_line(self, line, value):
       self.FPI_A[line] = self.FPI_A[line] * value
       self.FPI_b[line] = self.FPI_b[line] * value
       self.FPI_op_matrix[line] = self.FPI_op_matrix[line] * value

   def divide_line(self, line, value):
       self.FPI_A[line] = self.FPI_A[line] / value
       self.FPI_b[line] = self.FPI_b[line] / value
       self.FPI_op_matrix[line] = self.FPI_op_matrix[line] / value

   def add_lines(self, line1, line2, case):
       if(case == 0):
           self.FPI_A[line1] = self.FPI_A[line1] + self.FPI_A[line2]
           self.FPI_b[line1] = self.FPI_b[line1] + self.FPI_b[line2]
           self.FPI_op_matrix[line1] = self.FPI_op_matrix[line1] + self.FPI_op_matrix[line2]
       else:
           self.FPI_c = self.FPI_c + self.FPI_A[line2]
           self.FPI_y = self.FPI_y + self.FPI_op_matrix[line2]

#Returns a tuple that has matrix A and vector b
def split_b(matrix):
    A = [line[:-1] for line in matrix]
    b = [line[-1] for line in matrix]
    return A, b

#Test function, prints all
def print_test(progL):
    progL.displayA()
    progL.displayb()
    progL.displayc()
    progL.displayDimensoes()
    progL.display_FPI()
