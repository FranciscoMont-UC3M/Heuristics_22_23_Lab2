import sys
import json
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

with open("ASTAR-tests/" + students_path + ".prob") as textFile:
    data = textFile.read()
    print(data)

students_content = json.loads(data)
array_students = []
# We need to extract qualities of each
for k, v in students_content.items():
    array_students.append(k)
    print('student=', k, ', value=', v)

'''matrix_students = []
for i in range(len(array_students)):
    temp_student_array = array_students[i].split(",")
    matrix_students.append(temp_student_array)
print(matrix_students)
# print(matrix_students[0][0])'''

last_node_id = 0


class Node:
    def __init__(self, node_id, prev, depth, queue, gcost, student_id):
        self.id = node_id
        self.prev = prev
        self.depth = depth  # len(queue), will be depth of previous node + 1
        self.queue = queue  # an array storing the assigned students for this node, the queue state for this node
        self.gcost = gcost  # cost from initial node to current node, calculated on creation of node
        # self.hcost = 1+len(array_students)-depth  # cost estimation from current node to end, DEPENDS ON HEURISTIC
        self.student_id = student_id  # an array storing the cost for this node, inputted on node creation

    def get_id(self):
        return self.id

    def get_prev(self):
        return self.id

    def get_depth(self):
        return self.depth

    def get_queue(self):
        return self.queue

    def get_cost(self):
        return self.cost

    def get_student_id(self):
        return self.student_id


def get_cost_new_node(old_node, new_student):
    new_id = last_node_id + 1


