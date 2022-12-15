import sys
import ast
from queue import *
import time

'''Run cd parte-2 before running this python script'''

# This code reads the number of arguments given when running the script ("python arguments"), where
# 1st argument is the name of this python script,
# 2nd is the path of a solution for students placement,
# 3rd is the heuristic chosen for the ASTAR algorithm to calculate remaining cost to the final node
if len(sys.argv) != 3:
    print(sys.argv)
    sys.exit("Invalid amount of arguments to start the program")
students_path = sys.argv[1]
# print(sys.argv[1])
heuristic = sys.argv[2]
# print("heuristic chosen is: "+str(sys.argv[2]))

# We open the file with the list of assigned seats
with open("ASTAR-tests/" + students_path + ".prob") as textFile:
    data = textFile.read()
    students_content = ast.literal_eval(data)
    # print("original data "+str(data))
    print("formatted data "+str(students_content))

# We want to make the seats of each student more accessible.
# Student with id = x has array position x-1 in both cases
array_students = []
array_students_seats = []
matrix_students = []
# Add each student to the array/matrix corresponding
for student, seat in students_content.items():
    array_students.append(student[0])
    # First item is student_id, second its their assigned seat
    array_student_seat = [student[0], seat]
    array_students_seats.append(array_student_seat)
    # store characteristics of student into array: student_id, student_conflictive, student_restricted
    array_characteristics = [student[0], student[1], student[2]]
    matrix_students.append(array_characteristics)
# print(array_students)
print(array_students_seats)
print(matrix_students)

# Count number of reduced mobility and troublesome students
total_students = len(array_students)
total_reduced = 0
total_trouble = 0
for i in range(len(matrix_students)):
    if matrix_students[i][1] == "C":
        total_trouble += 1
    if matrix_students[i][2] == "R":
        total_reduced += 1
# print(total_students)
# print(total_reduced)
# print(total_trouble)


max_depth = len(array_students)
last_node_id = 0


class Node:
    def __init__(self, node_id, prev, depth, queue, remaining, gcost, hcost, student_id):
        self.id = node_id
        self.prev = prev  # The id for the previous node, to build a path if necessary
        self.depth = depth  # alternatively just len(queue), will be depth of previous node + 1
        self.queue = queue  # an array storing the assigned students for this node, the queue state for this node
        self.remaining = remaining  # an array storing the not yet visited students
        self.gcost = gcost  # cost from initial node to current node, calculated on creation of node
        self.hcost = hcost  # cost estimation from current node to end, DEPENDS ON HEURISTIC
        self.fcost = gcost+hcost  # total cost estimation (real previous cost + cost estimation)
        self.student_id = student_id  # the id of the student AS A STRING, LIKE IN ALL ARRAYS

    def get_id(self):
        return self.id

    def get_prev(self):
        return self.id

    def get_depth(self):
        return self.depth

    def get_queue(self):
        return self.queue

    def get_remaining(self):
        return self.remaining

    def get_gcost(self):
        return self.gcost

    def get_hcost(self):
        return self.hcost

    def get_fcost(self):
        return self.fcost

    def get_student_id(self):
        return self.student_id


'''Best First Search - A*, but we don't know the final state'''
def A_star_algorithm():
    empty_queue = []
    # Initial node attributes (node_id, prev_node_id, depth,
    #                           queue, remaining,
    #                           gcost, hcost, student_id)
    initial_node = Node(last_node_id, None, 0,
                        empty_queue, array_students,
                        0, heuristic_from_inputs(heuristic, empty_queue), None)
    open_list = [initial_node]  # Array of node_id/state, priority queue?
    closed_list = []  #
    success = False
    lowest_cost_node = initial_node

    while len(open_list) != 0 and success is False:
        # We find the lowest cost node, called N in the slides, and move it out of open_list and into closed_list
        lowest_cost_node = find_lowest_cost(open_list)
        open_list.remove(lowest_cost_node)
        closed_list.append(lowest_cost_node)
        # If it is lowest cost and also has no students left to enqueue [hcost = 0], then it is our goal node. Success!
        if lowest_cost_node.hcost == 0:
            success = True
        # Else, expand N = find successor nodes, create successor nodes if valid students, move them to open list
        # Our nodes only have one possible ancestor, so no repetitions possible.
        else:
            # expand_node returns a list with the valid nodes created after expanding, so we insert them
            list_new_nodes = expand_node(lowest_cost_node)
            for node in list_new_nodes:
                open_list.append(node)
            # Note that we don't reorder our open list by costs, we search for the lowest cost every time.
            # TODO: We could have made a sorting algorithm but run out of time.
    if success:
        final_queue = lowest_cost_node.get_queue()
        if len(final_queue) == 0:
            print("No inputs, only initial node")
        return final_queue


'''Search heuristics to find the lowest cost node'''
# Used to find lowest cost when we need to decide what node to expand
def find_lowest_cost(array_nodes):
    first_node = array_nodes[0]
    best_node = first_node
    best_cost = first_node.get_fcost()
    for node in array_nodes:
        node_fcost = node.get_fcost()
        if node_fcost < best_cost:
            best_cost = node_fcost
            best_node = node
    return best_node

# Like find_lowest_cost function, but it requires that the depth of the node be maximum (all students are in queue)
def find_lowest_cost_solution(array_nodes):
    first_node = array_nodes[0]
    best_node = first_node
    best_cost = first_node.get_fcost()
    for node in array_nodes:
        # Only if node is max depth is it a valid solution
        if node.get_depth() == max_depth:
            node_fcost = node.get_fcost()
            if node_fcost < best_cost:
                best_cost = node_fcost
                best_node = node
    return best_node


'''Node expansion, new node's queue validity, and gcost calculation functions'''
# We check that the possible new nodes are valid: R cant be final node, if previous was R we need non-R - WORKS
def queue_valid(queue):
    if queue is None:
        return True
    length_queue = len(queue)
    # If queue length is not bigger than zero (it is zero), then its initial case, we always expand it
    if length_queue > 0:
        # If we have a full queue we check final student because R cant be final node (nobody helps push them)
        if length_queue == len(array_students):
            id_last_student = queue[length_queue - 1]
            if id_last_student is not None and matrix_students[int(id_last_student)-1][2] == "R":
                return False
        # If previous to our student was R, we can't be R
        if length_queue > 1:
            id_last_student = queue[length_queue - 1]
            id_2nd_last_student = queue[length_queue - 2]
            if matrix_students[int(id_2nd_last_student)-1][2] == "R" and \
                    matrix_students[int(id_last_student)-1][2] == "R":
                return False
    return True

# We create all possible new queues with remaining students. If they are valid, create node and add it to list
def expand_node(expanding_node):
    list_new_nodes = []
    current_queue = expanding_node.get_queue()
    # Creation of all possible new queues with remaining students. If they are valid, create node and add it to list
    # print("remaining = "+str(expanding_node.get_remaining()))
    remaining_students = expanding_node.get_remaining()
    for i in range(len(remaining_students)):
        student_id = remaining_students[i]
        # the new queue is just the old queue without the student id we will be adding
        new_queue = []
        if current_queue is None:
            new_queue.append(student_id)
        else:
            new_queue = current_queue[:]
            new_queue.append(student_id)
        # If the new_queue is valid, create node and add it to list
        if queue_valid(new_queue) is True:
            new_id = last_node_id + 1  # Constantly increasing the node_id we will use
            prev_id = expanding_node.get_id()
            new_depth = expanding_node.get_depth() + 1
            # The remaining students are previous ones minus our new student
            new_remaining = remaining_students[:]
            new_remaining.remove(student_id)
            # Using the gcost function that calculates all previous cost and our own cost
            new_gcost = gcost(new_queue)
            # Using heuristic determined by inputs to estimate the cost until reaching a solution
            new_hcost = heuristic_from_inputs(heuristic, new_queue)
            # Create node with all new parameters for our new student id
            new_node = Node(new_id, prev_id, new_depth, new_queue, new_remaining, new_gcost, new_hcost, student_id)
            list_new_nodes.append(new_node)
    # If the queue for the node is valid, we create the node per se and append to the list
    return list_new_nodes

def gcost(queue):
    if queue is None:
        return 0
    cost_array = []
    # Default value for elements in cost array is 1, we create cost array
    for i in range(len(queue)):
        cost_array.append(1)
    # Depending on what type of student is sitting, and the ones before/after, costs get altered.
    # See below:
    for i in range(len(queue)):
        student_of_matrix = matrix_students[int(queue[i])-1]
        # Reduced mobility students have cost 3, but person behind them costs zero.
        if student_of_matrix[2] == "R":
            cost_array[i] = 3
            # i+1 should exist to push R due to queue_validity, but for tests purposes, this check is left here
            if i + 1 < len(cost_array):
                cost_array[i+1] = 0
        # Conflictive students double cost of the students before and after, and
        # they also double cost of any student after them in the queue who has a larger seat number
        if student_of_matrix[1] == "C":
            # Conflictive students double costs before and after them
            # if i-1 is lower than zero, we would change last element of the list.
            if i-1 >= 0:
                cost_array[i-1] *= 2
            # if i+1 is not smaller than array length, we would go out of array size and get an error.
            if i+1 < len(cost_array):
                cost_array[i+1] *= 2
            # Find conflictive student's seat value in array_students_seats,
            # because anyone after him in queue with higher number has double cost
            conflictive_seat = int(array_students_seats[int(queue[i])-1][1])
            # Check only queue students AFTER conflictive student, store their seat value
            for j in range(i+1, len(queue)):
                other_student_seat = int(array_students_seats[int(queue[j])-1][1])
                # If student after conflictive in queue has larger seat number, twice the cost for them
                if other_student_seat > conflictive_seat:
                    cost_array[j] *= 2
    # Computing final value of g(n) cost from initial to current node, so it can be stored in node attribute gcost
    total_gcost = 0
    for i in range(len(cost_array)):
        # print(str(i)+" costs "+str(cost_array[i]))
        total_gcost += cost_array[i]
    return total_gcost


'''Heuristics chosen and their functions'''
# Depending on the heuristic chosen when running, it calculates h(n) with different functions
def heuristic_from_inputs(heuristic, queue):
    hcost = 0  # If no valid heuristic chosen
    if heuristic == "1":
        hcost = heuristic1(queue)
    elif heuristic == "2":
        hcost = heuristic2(queue)
    return hcost

# Heuristic 1 is very basic: it adds one (minimum avg cost) for every student that remains to be inserted in the queue
def heuristic1(queue):
    # For initial case
    if queue is None:
        length_queue = 0
    else:
        length_queue = len(queue)
    hcost = len(array_students) - length_queue
    # print("hcost = "+str(hcost)+", for queue: "+str(queue))
    return hcost

# Heuristic 2 is a better aproximation than heuristic 1 for the minimum remaining cost:
# cost = 3 * number_reduced + 1 * (total - 2 * number_reduced)
# because reduced students cost 3 and non-reduced who aren't pushing a reduced (n-r-r) cost 1
def heuristic2(queue):
    # For initial case
    if queue is None:
        length_queue = 0
    else:
        length_queue = len(queue)

    reduced_in_queue = 0
    for i in range(length_queue):
        # We find in the matrix the student whose queue id is string i (so, the one in position int(i)-1),
        # and if they are reduced mobility we add one to the total of reduced in queue
        if matrix_students[int(queue[i])-1][2] == "R":
            reduced_in_queue += 1
    remaining_reduced = total_reduced - reduced_in_queue
    min_cost = 3 * (remaining_reduced) + 1 * (total_students - 2 * remaining_reduced)
    return min_cost


'''OUTPUT AREA'''
print("best solution is: "+str(A_star_algorithm()))




'''THE TEST ZONE - SCARY'''
'''# Testing queue_validity with students02 - False, 2 restricted need someone to push
# Testing queue_validity with students24 - True, restricted must go first
my_queue = ['1', '2']
print(str(my_queue)+" order validity is "+str(queue_valid(my_queue)))
# Testing queue_validity with students02 - False, 2 restricted need someone to push
# Testing queue_validity with students24 - False, restricted must go first
my_queue2 = ['2', '1']
print(str(my_queue2)+" order validity is "+str(queue_valid(my_queue2)))

# Testing gcost with students24 - cost = 3, correct
# Testing gcost with students23 - cost = 3, no
cost1 = gcost(my_queue)
print("gcost with "+str(my_queue)+" is "+str(cost1))
cost2 = gcost(my_queue2)
print("gcost with "+str(my_queue2)+" is "+str(cost2))'''

'''my_queue3 = ['1', '2', '3']  # ideal case for students31, cost = 4, CORRECT
cost3 = gcost(my_queue3)
print("gcost with "+str(my_queue3)+" is "+str(cost3))
my_queue4 = ['1', '3', '2']  # worst case for students31, cost = 8, CORRECT
cost4 = gcost(my_queue4)
print("gcost with "+str(my_queue4)+" is "+str(cost4))'''


