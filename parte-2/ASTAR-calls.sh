#!/bin/bash
# Copy and paste to execute after doing a "cd parte-2" to access to folder appropriately
python ASTARBusQ.py students02 1
# Test with 2 reduced mobility students, must fail, used to check queue_validity function successfully
python ASTARBusQ.py students04 1
# Test with 3 students (one troublesome, no reduced mobility)
python ASTARBusQ.py students23 1
# Test with 2 students (one troublesome), must work as 1CX and 2XX in whatever order, with cost = 3
python ASTARBusQ.py students24 1
# Test with 2 students (one reduced mobility), must work as 1XR first and 2XX second, with cost = 3
python ASTARBusQ.py students31 1
# Test with 3 students (one reduced mobility, one troublesome, one normal), must work as 1XR, 2XX, 3CX, with cost = 4
# {'1XR': 20, '2XX': 18, '3CX': 17}