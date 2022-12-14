from math import comb
import sys
import constraint
from constraint import *
import copy
import os
import time

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

array_students = []
with open("CSP-tests/" + students_path + ".txt") as textFile:
    for line in textFile:
        array_students.append(line.strip())
# print(array_students)
matrix_students = []
for i in range(len(array_students)):
    temp_student_array = array_students[i].split(",")
    matrix_students.append(temp_student_array)
print("matrix_students: "+str(matrix_students))
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

'''Add variables (student_id's) and their domains to the problem, domain array is set considering reduced mobility mobility'''
for i in range(len(matrix_students)):
    # print("element in row "+str(i)+" has restriction variable "+str(matrix_students[i][3]))
    if matrix_students[i][3] == 'X':
        problem.addVariable(matrix_students[i][0], domainWhite + domainBlue)
    elif matrix_students[i][3] == 'R':
        problem.addVariable(matrix_students[i][0], domainBlue)


'''Constraint checks that the seats assigned from domain are a single seat not assigned repeatedly - WORKS'''
# The solver algorithm already gives a single value to each variable,
# shows multiple possible values as different solutions
def uniqueSingleSeat(*args):
    for i in range(len(args)):
        for j in range(i+1, len(args)):
            if i != j and args[i] == args[j]:  # if different variables with same domain (sharing seat), not valid
                return False
    return True
problem.addConstraint(uniqueSingleSeat, arrayVariables)
# Alternatively, can use allDifferentConstraints function, identical role

'''Constraint for reduced mobility, is valid only if the seat adjacent to the free blue one assigned is also free - WORKS'''
# An IMPORTANT computational improvement would be to always seat them on the windows (seats 1+4k or 0+4k),
# since it will always be the best position for them taking into account constraints for troublesome students,
# but since it isn't a requirement, we will keep the more elemental version of the constraint for reduced mobility students.
def ifReducedmobilityThenAdjacentSeatIsFree(*args):
    for i in range(len(args)):
        #If i is reduced mobility student, then find if anyone is in adjacent blue (False=invalid)
        if matrix_students[i][3]=="R":
            valueReducedmobility = args[i]
            # print("current valueReducedmobility is "+str(valueReducedmobility))
            for j in range(i+1, len(args)):
                if valueReducedmobility % 2 == 0 and args[j] == valueReducedmobility - 1: #When sit on left empty
                    return False
                if valueReducedmobility % 2 == 1 and args[j] == valueReducedmobility + 1: #When sit on right empty
                    return False
    return True  # if no reduced mobility fails, there are no reduced mobility, or no variables, then constraint satisfied
problem.addConstraint(ifReducedmobilityThenAdjacentSeatIsFree, arrayVariables)

'''Constraint for troublesome, valid only if seats around not used by troublesome/reduced mobility, except if their sibling - WORKS'''
def ifTroublesomeNoCR_ExceptSibling(*args):
    for i in range(len(args)):
        # If i is troublesome student, then find if anyone is adjacent troublesome/reduced mobility who aren't brothers
        if matrix_students[i][2] == "C":
            valueTrouble=args[i]
            sibling_of_i=matrix_students[i][4] # Take sibling id
            for j in range(i+1, len(args)):
                # matrix_students[j][0] is the student id of j
                # If j is the sibling of i, or they are not troublesome/reduced mobility, they can seat without distance
                # For any other case, we need to check if student j is seated around i.
                # if matrix_students[j][0] == sibling:
                #    print("true sibling in position "+str(j))
                if matrix_students[j][0] != sibling_of_i and (matrix_students[j][2] == "C" or matrix_students[j][3] == "R"):
                    # print("if j+1 "+str(j+1)+" is equal to sibling "+str(sibling)+" this should not run")
                    valueOther=args[j]
                    # -4 and +4 checked in every case, if j is in their position, then constraint not satisfied
                    if valueTrouble-4 == valueOther or valueTrouble+4 == valueOther:
                        return False

                    # if i is sitting in the 1st row (left window), we need to check positions -4,-3,+1,+4,+5
                    elif valueTrouble % 4 == 1:
                        if valueTrouble-3 == valueOther or valueTrouble+1 == valueOther or valueTrouble+5 == valueOther:
                            return False
                    # if i is sitting in the 2nd or 3rd row (corridor), we need to check -5,-4,-3,-1,+1,+3,+4,+5
                    elif valueTrouble % 4 == 2 or valueTrouble % 4 == 3:
                        if valueTrouble-5 == valueOther or valueTrouble-3 == valueOther or \
                                valueTrouble-1 == valueOther or valueTrouble+1 == valueOther or \
                                valueTrouble+3 == valueOther or valueTrouble+5 == valueOther:
                            return False
                    # if i is sitting in the 4th row (right window), we need to check positions -5,-4,-1,+3,+4
                    elif valueTrouble % 4 == 0:
                        if valueTrouble-5 == valueOther or valueTrouble-1 == valueOther or valueTrouble+3 == valueOther:
                            return False
                    #return True  # If j not around i, then constraint satisfied
                #return True  # If j is sibling or it's not Troublesome/reduced mobility
        #return True  # If the student is not Troublesome, then constraint doesn't apply/satisfied
    return True
problem.addConstraint(ifTroublesomeNoCR_ExceptSibling, arrayVariables)

'''Constraint for year, valid only if 1st year in seats 1-16, and if 2nd year in 17-32 except if 1st year sibling - WORKS'''
arrayFrontBus = []  # For those who will have the constraint of sitting in seats 1-16
arrayBackBus = []  # For those who will have the constraint of sitting in seats 17-32
for i in range(len(arrayVariables)):
    # if the students are of first year they always sit on the front of the bus
    if matrix_students[i][1] == "1":
        arrayFrontBus.append(arrayVariables[i])
    # If they have a sibling in 1st year, they seat in the front of the bus with them, else they seat in the back
    elif matrix_students[i][1] == "2":
        sibling = int(matrix_students[i][4])
        if sibling != 0 and matrix_students[sibling-1][1] == "1":
            arrayFrontBus.append(arrayVariables[i])
        else:
            arrayBackBus.append(arrayVariables[i])
    # If they had to be on a seat on the FRONT of the bus (bus seat number under 17) and some seat is over 16, return False
    # If they had to be on a seat on the BACK of the bus (bus seat number over 16) and some seat is under 17, return False
print("Students sitting in the front of the bus: " + str(arrayFrontBus))
print("Students sitting in the back of the bus: " + str(arrayBackBus))

'''Constraint for siblings, valid only if they sit in same section - WORKS'''
def seatAccordingToYear_ExceptSibling(*args):
    for i in range(len(args)):
        # if the students are of first year they must sit on the front of the bus (seats 1-16), else failed constraint
        if matrix_students[i][1] == "1" and args[i]>16:
            return False
        # If they have a sibling in 1st year they must sit in the front of the bus with them (seats 1-16), else failed constraint
        elif matrix_students[i][1] == "2":
            sibling = int(matrix_students[i][4])
            if sibling != 0 and matrix_students[sibling - 1][1] == "1":
                if args[i]>16:
                    return False
            elif args[i]<17:
                return False
    return True
problem.addConstraint(seatAccordingToYear_ExceptSibling, arrayVariables)

'''Constraint for siblings, valid only if they sit together with the older one outside - WORKS'''
def ifSiblingSeatTogether_ExceptReducedmobility(*args):
    for i in range(len(args)):
        # if the student has a sibling, neither is reduced mobility and they're not sitting together then failed constraint
        # (remember x-1 is array position of student with id x)
        sibling_of_i = matrix_students[i][4]
        position_sibling = int(sibling_of_i)-1
        # If they are siblings and not reduced mobility
        if sibling_of_i != "0" and matrix_students[i][3] != "R" and matrix_students[position_sibling][3] != "R":
            # To know if they are sitting together, we store their positions, compare the difference and their values.
            pos_i = args[i]
            pos_j = args[position_sibling]
            # If difference between pos_i and pos_j is other than one, they are too far to be seated together.
            if abs(pos_i-pos_j) != 1:
                return False
            # If pos_i is in 4+4k and pos_j is larger by one (5+4k=1+5k), they are in different rows
            elif pos_i < pos_j and pos_i % 4 == 0:
                return False
            # If pos_i is in 1+4k and pos_j is smaller by one (4+3k), they are in different rows
            elif pos_i > pos_j and pos_i % 4 == 1:
                return False

            # To know if they are sitting together with older one outside, we find the older one (if there is any).
            age_i = int(matrix_students[i][1])
            age_j = int(matrix_students[position_sibling][1])
            age_dif = abs(age_i - age_j)
            if age_dif == 1:
                if age_i > age_j:  # When i older than j
                    # If i (older) in 2+4k and brother not in 1+4k then False.
                    if pos_i % 4 == 2 and pos_j % 4 != 1:
                        return False
                    # If i (older) in 3+4k and brother not in 0+4k then False.
                    if pos_i % 4 == 3 and pos_j % 4 != 0:
                        return False
                if age_j > age_i:  # When j older than i
                    # If j (older) not in 2+4k and then not in 3+4k, its in 1+4k or 0+4k, which arent seats near aisle
                    if pos_j % 4 != 2 and pos_j % 4 != 3:
                        if pos_i % 4 == 2 or pos_i % 4 == 3:
                            return False
            # if age difference is not 1 (they have the same age), we must check they are on the same side of aisle
            else:
                if pos_i % 4 == 2 and pos_j % 4 == 3:
                    return False
                if pos_i % 4 == 3 and pos_j % 4 == 2:
                    return False
    return True
problem.addConstraint(ifSiblingSeatTogether_ExceptReducedmobility, arrayVariables)

time_start = time.time()
# print(problem.getSolutions())

solutions = problem.getSolutions()
# print(problem.getSolutions()[1])

'''OUTPUT FILE'''
# We first find the number of solutions and make the string we will include at the start of the file
number_solutions = "Number of solutions:<"+str(len(solutions))+">"
solutions_final = str(number_solutions)+"\n"

# Then, we traverse the list of solutions and the student items within them, and create a string line for every solution
for index in range(len(solutions)):
    string_solution = solutions[index]
    string_final = "{"
    for k, v in string_solution.items():
        student = k+str(matrix_students[int(k)-1][2])+str(matrix_students[int(k)-1][3])
        seat = v
        student_string = "'"+student+"': "+str(seat)+", "
        string_final += student_string
    # Before ending line remove the last comma and space (of the last student item) so it fits the output guidelines
    string_final = string_final[:-2]
    string_final += "}\n"
    solutions_final += string_final

# Then we print the solutions that we will write into the output file
print(solutions_final)

# We write our string with the solutions in an output file
with open("CSP-tests/" + students_path + ".output", 'a') as outputFile:
    outputFile.write(solutions_final)

time_end = time.time()
print("Time from search of solutions to writing output, both included (seconds): "+str(time_end-time_start))
