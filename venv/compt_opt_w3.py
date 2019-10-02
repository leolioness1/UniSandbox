#import packages
from random import randint

#helper fuctiion

def decimal_to_binary_array(number):
    sol= list(map(int,bin(number)[2:]))
    return sol

#what is the problem?
#find in a interval of numbers 0 to 15 ,which is the one with the largest number of 1s in binary representations
#maximise the value
#buildingb blocks 1.decision variables

decision_variables ={'Numbers':list(range(0,16))}

#2.solution representation and encoding size of solution is 1 and is unordered (less possible permutations)
#[0,15] min-max
encoding = [0,15]

#3.build solution function -we will be generate a random number

def build_solution (encoding,decision_variables):
    max = encoding[-1]
    min = encoding[0]

    i = randint(min,max) # << generated randomly

    return i

#test the solution function

solution_test = build_solution(encoding=encoding, decision_variables=decision_variables)
print(f"i: {solution_test} binary representation { decimal_to_binary_array (solution_test)}")


#4.objective function - evaluates the performance of a solution it doesn't know if it is a max or min problem

def objective_function( solution, decision_variables ={}):
    fitness= 0
    binary_rep =decimal_to_binary_array (solution)
    for digit in binary_rep:
        fitness += digit # fitness = fitness + digit

    return fitness

#objective of the Fitness Function
objective = "Maximise"

#test the objective function

objective_test = objective_function(solution=solution_test, decision_variables=decision_variables)
print(f"Fitness: {objective_test} binary representation { decimal_to_binary_array (solution_test)}")


#5. constraints - in this example implocot constraint of the range of numbers (optional)
#illustrative

constraints = {"Min-i" : 0, "Max-i" : 15}

#6.solution admissibility funtion (optional)
#illustrative

def is_admissable( solution, constraints ={}, decision_variables = {}):
    min =0
    if "Min-i" in constraints: min =constraints["Min-i"]
    max = 0
    if "Max-i" in constraints: max = constraints["Max-i"]

    return  solution >= min and solution <= max

print(f"Solution: {solution_test} Is admissable: {is_admissable(solution_test,constraints=constraints, decision_variables=decision_variables)}")

#7.neighbourhood function - generates a neighbourhood of a current solution

def get_neighbours( solution, decision_variables ={}):
    numbers = decision_variables ["Numbers"]

    if solution ==numbers[0]:
        return [solution + 1]
    elif solution == numbers [-1]:
        return [solution -1]
    else:
        return  [solution -1, solution + 1 ]

#test neighbourhood function
print(f"Solution: {solution_test} Neighbours: {get_neighbours(solution_test,decision_variables=decision_variables)}")

def best_neighbour(initial_solution,decision_variables):
    fitness_solution = objective_function(initial_solution, decision_variables=decision_variables)
    neighbours= get_neighbours(initial_solution,decision_variables=decision_variables)
    for i in neighbours:
        fitness_i= objective_function(i,decision_variables=decision_variables)
        if fitness_i >= fitness_solution:
            solution ={"solution":i, "fitness":fitness_i}
            best_neighbour_exit=True
        else:
            solution = ["There are no neighbours with better fitness",initial_solution,fitness_solution]
    return solution, best_neighbour_exit

print(best_neighbour(solution_test,decision_variables=decision_variables))


import numpy as np
from random import uniform
np.exp(-abs(fitness_solution - fitness_neighbour)/cp)

0.34 <np.exp(-2)

# Data
f_j = 10
f_i = 11
CP = 1
print("Excercise:\n--------------------------------------------")
# Calculate the Probability
probability = np.exp( - ( abs( f_j - f_i ) / CP ) )
print(f"Probability = {probability}")
# Event probability: Accept or Reject
random_num = uniform(0,1)
if random_num <= probability:
    print(f"Accepted! | random_num {random_num} <= probability {probability}")
else:
    print(f"Rejected! | random_num {random_num} IS NOT <= probability {probability}")