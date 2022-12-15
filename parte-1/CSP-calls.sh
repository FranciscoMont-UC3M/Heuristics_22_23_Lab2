#!/bin/bash
# Copy and paste to execute after doing a "cd parte-1" to access to folder appropriately
python CSPBusSeats.py students01
# test with a single restricted on the back - 4 solutions (constraints work)
python CSPBusSeats.py students02
# test with two restricted (one troublesome) on the back - 6 solutions (constraints work)
python CSPBusSeats.py students21
# test with two restricted brothers (one troublesome) on front,back (=on front) -
# 48 (8x6) solutions (constraints work)
python CSPBusSeats.py students22
# test with two brothers (one troublesome) on front,back (=on front) -
# 8 solutions (constraints work)
python CSPBusSeats.py students23
# test with two brothers (one troublesome) on front (same year) -
# 16 solutions (constraints work)
python CSPBusSeats.py students24
# test for ASTAR with two students (one restricted and one non-restricted) on back -
# 56 (4x14) solutions (constraints work)
python CSPBusSeats.py students03
# test should fail - three restricted & troublesome in the back where only 2 fit in 4 seats -
# 0 solutions (constraints work)
python CSPBusSeats.py students03
# test for ASTAR with three students (one restricted, one normal, and one conflictive) in the back -
# 728 solutions
python CSPBusSeats.py students04
# test with four restricted and troublesome students (2 first year, 2 second year) -
# 36 (6x6) solutions (constraints work)
python CSPBusSeats.py students41
# test with four restricted & troublesome (3 in the back, one on the front which has brother in the back) -
# 48 (8x6) solutions (constraints work)

python CSPBusSeats.py students06
# test should fail - six restricted and troublesome students (only space for four)
# 0 solutions (constraints work)
python CSPBusSeats.py students08
# test with eight students, copied from the statement
#