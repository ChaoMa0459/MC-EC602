"""this is the main part of the assignment"""

# Copyright mc163@bu.edu

import unittest
import subprocess

#please change this to valid author emails
AUTHORS = ['mc163@bu.edu']

#PROGRAM_TO_TEST = "cf/collisionc_26_hard"
PROGRAM_TO_TEST = "cf/collisionc_27"

def runprogram(program, args, inputstr):
    coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)


class CollisionTestCase(unittest.TestCase):
    "empty class - write this"
#    def test_programname(self):
#        self.assertTrue(PROGRAM_TO_TEST.startswith('cf/collisionc'),"wrong program name")

    def test_one(self):
        strin = "A 20 10 -2 1"
        correct_out = "3\nA 14 13 -2 1\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")


    def test_bad_input(self):
        strin = "A 1 1"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        self.assertEqual(rc,1)
        self.assertEqual(out,"")
        self.assertEqual(errs,"")

    def test_empty(self):
        strin = ""
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,"3\n")
        self.assertEqual(errs,"")

    def test_value_not_number(self):
        strin = "A 1 1 1 A"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        self.assertEqual(rc,1)
        self.assertEqual(out,"")
        self.assertEqual(errs,"")

    def test_y_axis(self):
        strin = "A 0 0 0 10\nB 0 50 0 -10"
        correct_out = "4\nA 0 0 0 -10\nB 0 50 0 10\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["4"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_x_axis_collision_sametime(self):
        strin = "A 0 0 10 0\nB 50 0 -10 0\nC -10 0 10 0"
        correct_out = "4\nA 20 0 10 0\nB 50 0 10 0\nC 10 0 -10 0\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["4"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_many_xjbz(self):
        strin = "A 0 0 10 0\nB 50 0 -10 0\nC 25 25 0 -10"
        correct_out = "5.5\nA 17.928932 -37.071068 0 -10\nB 32.071068 -37.071068 0 -10\nC 25 44.142136 0 10\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["5.5"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".5000", ".5")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_negative(self):
        strin = "A 0 0 0 10\nB 0 50 0 -10"
        correct_out = "-1\nA 0 0 0 -10\nB 0 50 0 10\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["-1"],strin)
        self.assertEqual(rc,2)
        self.assertEqual(out,"")
        self.assertEqual(errs,"")

    def test_order(self):
        strin = "A 0 0 0 10\nB 0 50 0 -10"
        correct_out = "1\nA 0 10 0 10\nB 0 40 0 -10\n5\nA 0 -10 0 -10\nB 0 60 0 10\n"
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["5","1"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_large_input(self):
        strin = "one 1000000000000 0 1 0\ntwo 2100000000000 0 0 0"
        correct_out = "1000000\none 1.000001e+12 0 1 0\ntwo 2.1e+12 0 0 0\n"          
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1000000"],strin)
        self.assertEqual(rc,0)
        out = out.replace("1000000.0000", "1000000")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_decimal(self):	
        strin = "A 1.8 3.4 1 0\nB 14.4 2.1 -1 0"
        correct_out = "3\nA 1.5408859 3.827311 -0.9662 0.25779364\nB 14.659114 1.672689 0.9662 -0.25779364\n"      
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["3"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")

    def test_too_many(self):
        strin = "A 1 1 0 0\nB 1 -1 0 0\nC 12 5 0 0\nD 3 -1 0 0\nE 2 2 0 0\nF 1 1 2 3\nG 1 2 3 4\nH 4 -3 2 -1\nI 1 3 2 4\nJ 3 1 3 4\nK 1 1 1 1\nL 1 1 1 1\n"
        correct_out = "1\nA 1 1 0 0\nB 1 -1 0 0\nC 14.217597 5.3394628 3.5296 0.54030003\nD 3 -1 0 0\nE 2 2 0 0\nF 3 4 2 3\nG 1.7824029 5.6605372 -0.52959996 3.4597\nH 5.5820006 -2.6708467 0.5690912 3.55\nI 3.4179994 5.6708467 3.4309088 -0.55\nJ 6 5 3 4\nK 2 2 1 1\nL 2 2 1 1\n"     
        (rc,out,errs) = runprogram(PROGRAM_TO_TEST,["1"],strin)
        self.assertEqual(rc,0)
        out = out.replace(".0000", "")
        self.assertEqual(out,correct_out)
        self.assertEqual(errs,"")



def main():
    "show how to use runprogram"

#    print(runprogram('./test_program.py', ["4", "56", "test"], "my input"))
    unittest.main()

if __name__ == '__main__':
    main()
