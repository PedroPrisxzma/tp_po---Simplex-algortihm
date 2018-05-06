import numpy as np
import scipy
import sys
import fractions
import json
import pl

#The Programação Linear class
class PL:
   #Pl, constructor
   def __init__(self, A, c, b, n, m, input_pl):

       self.A = A #matrix A
       self.c = c #vector c
       self.b = b #vector b
       self.aux = input_pl

       #matrix A dimensions
       self.n = n #columns
       self.m = m #lines

       #FPI elements for the tableu
       self.FPI_A = 0
       self.FPI_b = 0
       self.FPI_c = 0
       self.FPI_y = 0
       self.FPI_op_matrix = 0
       self.vo = np.zeros(1)
       self.base = {} #dicionario contendo base {'linha': 'coluna'}
       self.input_pl = 0

   #Default prints
   def displayA(self):
       print("Matrix A\n",self.A)

   def displayc(self):
       print("Vector c\n",self.c)

   def displayb(self):
       print("Vector b\n",self.b)

   def displayDimensoes(self):
       print("linhas:",self.m,"colunas:", self.n)

   def display_base(self):
       print("Base Canonica\n", self.base)
   
   #Format FPI para o tableu
   def make_FPI(self):
       self.input_pl = np.zeros((self.m + 1, self.n + 1 + self.m))
       self.input_pl[:,:-self.m-1] = self.aux[:, :-1] 
       self.input_pl[1:,self.n:self.n+self.m] = np.identity(self.m)
       self.input_pl[:, self.n+self.m:] = self.aux[:, self.n:]
       self.input_pl[0] = self.input_pl[0] * -1

       #Faz matriz A da FPI
       self.FPI_A = np.zeros((self.m, self.n + self.m))
       self.FPI_A[:,:-self.m] = self.A
       self.FPI_A[:,self.n:] = np.identity(self.m)

       #Faz o vetor c
       self.FPI_c = np.zeros(self.n + self.m)
       self.FPI_c[:-self.m] = self.c * (-1)

       self.FPI_op_matrix = np.identity(self.m)
       self.FPI_y = np.zeros(self.m)
       self.FPI_b = self.b
       
       #arruma a base canonica inicial (nas variaveis de folga)
       j = 1
       for i in range(self.m, 0, -1):
           self.base[i-1] = (self.n + self.m - j)
           j += 1     

   def display_FPI(self):
       print("FPI A\n", self.FPI_A)
       print("FPI b\n", self.FPI_b)
       print("FPI c\n", self.FPI_c)
       print("FPI y\n", self.FPI_y)
       print("FPI Op\n", self.FPI_op_matrix)
       print("Valor Objetivo\n", self.vo)

   #operações na PL
   def multiply_line(self, line, value):
       self.FPI_A[line] = self.FPI_A[line] * value
       self.FPI_b[line] = self.FPI_b[line] * value
       self.FPI_op_matrix[line] = self.FPI_op_matrix[line] * value
       self.input_pl[line + 1] = self.input_pl[line + 1] * value

   def divide_line(self, line, value):
       self.FPI_A[line] = self.FPI_A[line] / value
       self.FPI_b[line] = self.FPI_b[line] / value
       self.FPI_op_matrix[line] = self.FPI_op_matrix[line] / value
       self.input_pl[line + 1] = self.input_pl[line + 1] / value

   def add_lines(self, line1, line2, value, case):
       if(case == 0):
           self.FPI_A[line1] = self.FPI_A[line1] + self.FPI_A[line2] * value
           self.FPI_b[line1] = self.FPI_b[line1] + self.FPI_b[line2] * value
           self.FPI_op_matrix[line1] = self.FPI_op_matrix[line1] + self.FPI_op_matrix[line2] * value
           self.input_pl[line1 + 1] = self.input_pl[line1 + 1] + self.input_pl[line2 + 1] * value
       else:
           self.FPI_c = self.FPI_c + self.FPI_A[line2] * value
           self.FPI_y = self.FPI_y + self.FPI_op_matrix[line2] * value
           self.vo = self.vo + self.FPI_b[line2] * value
           self.input_pl[0] = self.input_pl[0] + self.input_pl[line2 + 1] * value

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
    progL.display_base()