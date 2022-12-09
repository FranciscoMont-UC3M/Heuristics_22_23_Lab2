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

domainWhite = []
domainBlue = []
for i in range(len(array_bus)):
    if array_bus[i] == "blue":
        domainBlue.append(i)
    if array_bus[i] == "white":
        domainWhite.append(i)

# Add student variables (student_id's) and their domains to the solution, considering restricted mobility for domain
for i in range(len(matrix_students)):
    # print("element in row "+str(i)+" has restriction variable "+str(matrix_students[i][3]))
    if matrix_students[i][3] == 'X':
        problem.addVariable(matrix_students[i][0], domainWhite + domainBlue)
    elif matrix_students[i][3] == 'R':
        problem.addVariable(matrix_students[i][0], domainBlue)

