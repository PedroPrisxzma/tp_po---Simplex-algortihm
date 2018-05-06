import numpy as np
import scipy
import sys
import fractions
import json
import pl

#Função para escolher qual simplex aplicar
def simplex(progL):
    file_f = open('primeiro.txt', 'w')
    file_g = open('conclusao.txt', 'w')
    case = tipo_sol(progL)
    sol = np.zeros(progL.m + progL.n)
    print_step(progL, file_f)
    
    #primal
    if(case == 1):
        result = simplex_p(progL, file_f)
        #print to file
        if(result == 42):
            #dictionary to build solutiom
            for i in range(len(progL.base)):
                sol[progL.base[i]] = progL.FPI_b[i]    
            #print to file
            file_g.write("2\n")
            s = str(sol[:-progL.m]) 
            file_g.write(s)
            file_g.write("\n")
            vo = str(progL.vo)
            file_g.write(vo)
            file_g.write("\n")
            y = str(progL.FPI_y)
            file_g.write(y)
            file_g.write("\n")
        elif(result[0] == 3):
            #case unlimited
            file_g.write("1\n")
            #dictionary to help with certificate
            sol[result[1]] = 1
            for i in range(len(progL.base)):
                sol[progL.base[i]] = progL.FPI_A[i][result[1]] * -1
            s = str(sol[:-progL.m])
            file_g.write(s)
            file_g.write("\n")                          
    #dual
    elif(case == 2):
        result = simplex_d(progL, file_f)
        if(result == 42):
            #dictionary to build solution
            for i in range(len(progL.base)):
                sol[progL.base[i]] = progL.FPI_b[i]    
            #print to file
            file_g.write("2\n")
            s = str(sol[:-progL.m]) 
            file_g.write(s)
            file_g.write("\n")
            vo = str(progL.vo)
            file_g.write(vo)
            file_g.write("\n")
            y = str(progL.FPI_y)
            file_g.write(y)
            file_g.write("\n")
        elif(result[0] == 2):
             #case unfeasible
            file_g.write("1\n")
            #dictionary to help with certificate
            sol = progL.FPI_op_matrix[result[1]]
            s = str(sol)
            file_g.write(s)
            file_g.write("\n")
               
    #with aux
    elif(case == 3):
        result = simplex_aux(progL, file_f)        
    
    file_f.close()
    file_g.close()            

#Simplex Primal
def simplex_p(progL, file_f):
    while(1):
        state = pivo_primal(progL)
        if(state == 42):
            return state
            break
        elif(state[0] == 3):
            return state
            break    
        elif(state[0] == 1):
            sub_0 = progL.FPI_c[state[2]] / progL.FPI_A[state[1]][state[2]]
            progL.add_lines(state[1], state[1], sub_0 * -1, 1)
            for i in range(progL.m):
                if(i != state[1]):
                    sub_others = progL.FPI_A[i][state[2]] / progL.FPI_A[state[1]][state[2]]
                    progL.add_lines(i, state[1], sub_others * -1, 0)
            print_step(progL, file_f)


#simplex Dual
def simplex_d(progL, file_f):
    while(1):
        state = pivo_dual(progL)
        if(state == 42):
            return state
            break
        elif(state[0] == 2):
            return state
            break    
        elif(state[0] == 1):
            sub_0 = progL.FPI_c[state[2]] / progL.FPI_A[state[1]][state[2]]
            progL.add_lines(state[1], state[1], sub_0 * -1, 1)
            for i in range(progL.m):
                if(i != state[1]):
                    sub_others = progL.FPI_A[i][state[2]] / progL.FPI_A[state[1]][state[2]]
                    progL.add_lines(i, state[1], sub_others * -1, 0)                
            print_step(progL, file_f)


#Primal with aux
def simplex_aux(progL, file_f):
    new_c = np.zeros(progL.n + progL.m)
    progL_aux = pl.PL(progL.FPI_A, new_c, progL.FPI_b, progL.n + progL.m, progL.m, progL.input_pl)
    progL_aux.make_FPI()
    
    for i in range(progL.m):
        progL_aux.FPI_c[progL.n + progL.m:] = 1
    for i in range(progL.m):    
        progL_aux.add_lines(i, i, -1, 1)

    aux_result = simplex_p(progL_aux, file_f)
    print(aux_result)
   # pl.print_test(progL_aux)


#Define o tipo de simplex a ser aplicado
def tipo_sol(progL):
    if(all(i >= 0 for i in progL.FPI_b)):
        if(all(i >= 0 for i in progL.FPI_c)):
            print("Case B & C positives\n")
            return 42
        else:
            print("Case Primal\n")
            return 1
    else:
        if(all(i >= 0 for i in progL.FPI_c)):
            print("Case Dual")
            return 2
        else:
            print("Case Primal with aux, with b also negative")
            for x in range(len(progL.FPI_b)):
                if(progL.FPI_b[x] < 0):
                    progL.multiply_line(x, -1)
            return 3

#Funções que escolhem o pivo
def pivo_primal(progL):
    min = 1000000000 #min between b / (possible values of pivo)
    aux_min = 0 #current lowest value
    index_min = 0 #the chosen row index
    positivo = 1 #flag for no positive values in column
    column = choose_pivo_primal(progL)
    if(column >= 0):
        for i in range(progL.m):
            if(progL.FPI_A[i][column] > 0):
                positivo = 1
                break
            elif(progL.FPI_A[i][column] <= 0):
                positivo = -1
        if(positivo == -1):
                return (3, column) #caso ilimitada
        
    if(column >= 0):
        for i in range(progL.m):
            if(progL.FPI_A[i][column] > 0):
                aux_min = progL.FPI_A[i][column]
                aux_min = progL.FPI_b[i] / aux_min #finding lowest b / (possible values of pivo) 
                if(aux_min < min):
                    min = aux_min
                    index_min = i            
        att_base(progL, index_min, column)            
        progL.divide_line(index_min, progL.FPI_A[index_min][column])
        return (1, index_min, column) #continua simplex
    else:
        return 42 #end of simplex    

def pivo_dual(progL):
    min = 1000000000 #min between c / (possible values of pivo)
    aux_min = 0 #current lowest value
    index_min = 0 #the chosen column index
    inviável = -1 #Viability flag
    line = choose_pivo_dual(progL)
    if(line >= 0):
        for i in range(progL.n):
            if(progL.FPI_A[line][i] < 0):
                aux_min = progL.FPI_A[line][i] * -1
                aux_min = progL.FPI_c[i] / aux_min #finding lowest c / (possible values of pivo)
                inviável = 1
                if(aux_min < min):
                    min = aux_min
                    index_min = i
        if(inviável > 0):
            att_base(progL, line, index_min)
            progL.divide_line(line, progL.FPI_A[line][index_min])
            return (1, line, index_min) #continue simplex
        else: #case infeasible
            return (2, line) 
    else: #line < 0, no negative
        return 42 #end of simplex


#Functions that choose the row(dual) or column(primal) of the pivo
def choose_pivo_primal(progL):
    for i in range(len(progL.FPI_c)):
        if(progL.FPI_c[i] < 0):
            #column of pivo
            return i #index of coluna
    return -1 #no negatives

def choose_pivo_dual(progL):
    for i in range(len(progL.FPI_b)):
        if(progL.FPI_b[i] < 0):
            #row of pivo    
            return i #indice da linha
    return -1 #no negatives

#Base updating function
def att_base(progL, row, col):
    progL.base[row] = col

#Printing Function/
def print_step(progL, f):
    #prints each step on a file (primeiro.txt)
    f.write('{0}{1}'.format(progL.FPI_y, progL.input_pl[0]))
    f.write("\n")
    for i in range(1, progL.m+1):
        f.write('{0}{1}'.format(progL.FPI_op_matrix[i-1], progL.input_pl[i]))
        f.write("\n")
    f.write("\n")


#TODO:

#simplex dual, simplex primal com auxiliar

