#!/bin/bash
# Copy and paste to execute after doing a "cd parte-1" to access to folder appropriately
python CSPBusSeats.py students01 # test with a single restricted (constraints work up to troublesome, 5 and 6 remain)
python CSPBusSeats.py students02 # test with two restricted and one troublesome (constraints work up to troublesome, 5 and 6 remain)
python CSPBusSeats.py students03 # test with two restricted and one troublesome brothers (constraints work up to troublesome, 5 and 6 remain)

python CSPBusSeats.py students06 # test with six restricted and troublesome students
python CSPBusSeats.py students08 # test with eight students, copied from the statement