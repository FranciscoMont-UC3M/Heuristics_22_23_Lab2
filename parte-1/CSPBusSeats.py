from math import comb
import sys
import constraint
from constraint import *
import copy
import os

'''Run cd parte-1 before running this python script'''

# This code reads the number of arguments given when running the script ("python arguments"),
# where 1st argument is the name of this python script, 2nd is the path of the file with students data we have to read
if len(sys.argv) != 2:
    print(sys.argv)
    sys.exit("Invalid amount of arguments to start the program")
students_path = sys.argv[1]
# print(sys.argv[1])

# Seat array organized in numerical order. array_bus[i] is seat number i.
# The seats for reduced mobility students are the positions with value blue
# The seats near the aisle are the ones with position 2+4k and 3+4k
array_bus = ["blue", "blue", "blue", "blue",
             "white", "white", "white", "white",
             "white", "white", "white", "white",
             "blue", "blue", "blue", "blue",
             "blue", "blue", "blue", "blue",
             "white", "white", "white", "white",
             "white", "white", "white", "white",
             "white", "white", "white", "white"]


# The array of students stores all students as read from the file, in order.
# Student with id number 1 will be in position 0, and so on, id number i will be in position i-1 of the array.
'''This could be problematic if we didn't get id's in order or with jumps of number, 
    in which case we would need to store them in a list and create a find(id) function to search them. 
    For the sake of simplicity we assume the data is provided ordered and i-1 position is element with id i, but
    we could have made such version too, at higher computational time'''

array_students=[]
with open("CSP-tests/" + students_path + ".txt") as textFile:
    for line in textFile:
        array_students.append(line.strip())
# print(array_students)
matrix_students = []
for i in range(len(array_students)):
    temp_student_array = array_students[i].split(",")
    matrix_students.append(temp_student_array)
print(matrix_students)
# print(matrix_students[0][0])

problem = Problem()

# Domains with proper numbers for the seats (i+1 because arrays start on zero) depending on colour
domainWhite = []
domainBlue = []
for i in range(len(array_bus)):
    if array_bus[i] == "blue":
        domainBlue.append(i+1)
    if array_bus[i] == "white":
        domainWhite.append(i+1)
# print(domainBlue)
# print(domainWhite)

arrayVariables = []
for i in range(len(matrix_students)):
    arrayVariables.append(matrix_students[i][0])

'''Add variables (student_id's) and their domains to the problem, domain array is set considering restricted mobility'''
for i in range(len(matrix_students)):
    # print("element in row "+str(i)+" has restriction variable "+str(matrix_students[i][3]))
    if matrix_students[i][3] == 'X':
        problem.addVariable(matrix_students[i][0], domainWhite + domainBlue)
    elif matrix_students[i][3] == 'R':
        problem.addVariable(matrix_students[i][0], domainBlue)


'''Constraint checks that the seats assigned from domain are a single seat and not assigned repeatedly'''
def uniqueSingleSeat(*args):
    for i in range(len(args)):
        for j in range(i+1, len(args)):
            if i != j and args[i] == args[j]:  # if different variables with same domain (sharing seat), not valid
                return False
        if len(args[i] != 1):  # if using none/several seats, not valid
            return False
    return True

problem.addConstraint(uniqueSingleSeat, arrayVariables)

'''Constraint for restricted mobility is valid only if the seat assigned is blue and adjacent one is also free'''
def ifRestrictedThenSeatIsFreeBlue(*args):
    for i in range(len(args)):
        #If i is restricted student, then compare to all other ones (i!=j) and see if anyone is in adjacent blue
        for j in range(len(args)):
            if i != j and args[i] == args[j]:  # if different variables with same domain (sharing seat), not valid
                return False
        if len(args[i] != 1):  # if using none/several seats, not valid
            return False
    return False

def seatIsFreeBlue(a):
    if array_bus[a-1] == "blue":
        if a % 2 == 0 and seatIsUsed(a-1):
            return True
    return False

def seatIsUsed(b):
    for j in range(len(arrayVariables)):
        if matrix_students[j] == b:
            return True
    return False

'''
if 3 in domainBlue:
    print("3 in domainBlue")
'''
