from os import path
import unittest

from autograder_utils.Decorators import HTMLFormat, Number, OutputMessage, Weight
from autograder_utils.JSONTestRunner import JSONTestRunner
from autograder_utils.ResultBuilders import gradescopeResultBuilder
from autograder_utils.ResultFinalizers import gradescopeResultFinalizer

class Tests(unittest.TestCase):
    @OutputMessage()
    @Number("1.0")
    @Weight(1.0)
    def testSetOutput(self, set_output):
        """test_set_output"""
        set_output("Huzzah!")


    @OutputMessage()
    @HTMLFormat()
    @Number("2.0")
    @Weight(1.0)
    def testSetOutputHTML(self, set_output):
        """test_set_output_html"""
        set_output("Huzzah!")

    @Number("3.0")
    @Weight(1.0)
    def testFailure(self):
        """test_failure"""
        self.assertEqual(1, 2)

if __name__ == "__main__":

    tests = unittest.loader.makeSuite(Tests)

    with open("/autograder/results/results.json", 'w') as w:
        testRunner = JSONTestRunner(visibility='visible', stream=w,
                                    result_builder=gradescopeResultBuilder,
                                    result_finalizer=gradescopeResultFinalizer)

        res = testRunner.run(tests)
