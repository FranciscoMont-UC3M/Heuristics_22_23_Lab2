#!/bin/bash
# Copy and paste to execute after doing a "cd parte-1" to access to folder appropriately
python CSPBusSeats.py students01 # test with a single restricted (constraints work up to 5, and 6 remain)
python CSPBusSeats.py students02 # test with two restricted and one troublesome (constraints work up to 5, and 6 remain)
python CSPBusSeats.py students21 # test with two restricted and one troublesome brothers (constraints work up to 5, and 6 remain)
python CSPBusSeats.py students03 # test should fail - 3 restricted troublesomes in the back where only 2 fit
                                 # (constraints for restricted/trouble NOT WORKING - it gives solutions sitting them together)
python CSPBusSeats.py students04 # test with four restricted and troublesome students (2 first year, 2 second year)
                                 # (constraints for restricted and troublesome fail - 17,19,1,2 as solution)
python CSPBusSeats.py students06 # test with six restricted and troublesome students
python CSPBusSeats.py students07 # test with six restricted, troublesome students
python CSPBusSeats.py students08 # test with eight students, copied from the statement