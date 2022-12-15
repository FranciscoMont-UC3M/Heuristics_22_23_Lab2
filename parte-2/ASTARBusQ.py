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
matrix_students = []
# Add each student to the array/matrix corresponding
for student, seat in students_content.items():
    # First item is student_id, second its their assigned seat
    array_student_seat = [student[0], seat]
    array_students.append(array_student_seat)
    # store characteristics of student into array: student_id, student_conflictive, student_restricted
    array_characteristics = [student[0], student[1], student[2]]
    matrix_students.append(array_characteristics)
print(array_students)
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
    def __init__(self, node_id, prev, depth, queue, gcost, hcost, student_id):
        self.id = node_id
        self.prev = prev
        self.depth = depth  # len(queue), will be depth of previous node + 1
        self.queue = queue  # an array storing the assigned students for this node, the queue state for this node
        self.gcost = gcost  # cost from initial node to current node, calculated on creation of node
        self.hcost = hcost  # cost estimation from current node to end, DEPENDS ON HEURISTIC
                            # 1+len(array_students)-depth
        self.fcost = gcost+hcost
        self.student_id = student_id  # an array storing the cost for this node, inputted on node creation

    def get_id(self):
        return self.id

    def get_prev(self):
        return self.id

    def get_depth(self):
        return self.depth

    def get_queue(self):
        return self.queue

    def get_gcost(self):
        return self.gcost

    def get_hcost(self):
        return self.hcost

    def get_fcost(self):
        return self.fcost

    def get_student_id(self):
        return self.student_id


#Best First Search - A*, but we don't know the final state
def A_star_algorithm(state_of_n):
    empty_queue = []
    # Initial node with attributes (node_id, prev_node_id, depth, queue, gcost, hcost, student_id)
    initial_node = Node(last_node_id, None, 0, empty_queue, 0, heuristic_from_inputs(heuristic, empty_queue), None)
    open_list = [initial_node]  # Array of node_id/state, priority queue?
    closed_list = []  #
    success = False
    lowest_cost_node = initial_node

    while len(open_list)!=0 and success == False:
        # We find the lowest cost node, called N in the slides, and move it out of open_list and into closed_list
        lowest_cost_node = find_lowest_cost(open_list)
        open_list.remove(lowest_cost_node)
        closed_list.append(lowest_cost_node)
        # If it is lowest cost and also is
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
            # We could make a sorting algorithm but run out of time.
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


#TODO
'''Node expansion, new node's queue validity, and gcost calculation functions'''
def expand_node(expanding_node):
    list_new_nodes = []
    # create new possible queues
    # If the queue for the node is valid, we create the node per se and append to the list
    return list_new_nodes

# We check that the possible new nodes are valid: R cant be final node, if previous was R we need non-R
def queue_valid(queue):    
    length_queue = len(queue)
    # If queue length is not bigger than zero (it is zero), then its initial case, we always expand it
    if length_queue > 0:
        if length_queue == len(array_students):
            id_last_student = queue[length_queue - 1]
            # TODO: R cant be final node
            if id_last_student is not None and matrix_students[int(id_last_student)-1]:
                return False
        # TODO: if previous to us was R, we can't be R
            if length_queue > 1:
                id_2nd_last_student = queue[length_queue - 2]
                return False
    return True

'''Heuristics chosen and their functions'''
# Depending on the heuristic chosen when running, it calculates h(n) with different functions
def heuristic_from_inputs(heuristic, queue):
    if heuristic == "1":
        hcost = heuristic1(queue)
    elif heuristic == "2":
        hcost = heuristic2(queue)

# Heuristic 1 is very basic: it adds one (minimum avg cost) for every student that remains to be inserted in the queue
def heuristic1(queue):
    hcost = len(array_students) - len(queue)
    print("hcost = "+str(hcost)+", for queue: "+str(queue))
    return hcost

# Heuristic 2 is a better aproximation that heuristic 1 for the minimum remaining cost:
# cost = 3 * number_reduced + 1 * (total - 2 * number_reduced)
# because reduced students cost 3 and non-reduced who aren't pushing a reduced (n-r-r) cost 1
def heuristic2(queue):
    reduced_in_queue = 0
    for i in range(len(queue)):
        # We find in the matrix the student whose queue id is string i (so, the one in position int(i)-1),
        # and if they are reduced mobility we add one to the total of reduced in queue
        if matrix_students[int(queue[i])-1][2] == "R":
            reduced_in_queue += 1
    remaining_reduced = total_reduced - reduced_in_queue
    min_cost = 3 * (remaining_reduced) + 1 * (total_students - 2 * remaining_reduced)
    return min_cost

'''TODO'''
def get_cost_new_node(old_node, new_student):
    new_id = last_node_id + 1


