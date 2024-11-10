import unittest

from autograder_utils.ResultFinalizers import prairieLearnResultFinalizer

class VerifyPrairieLearnResultFinalizer(unittest.TestCase):
    @staticmethod
    def generateTestResults(maxPoints: float, actualPoints: float, numberOfTestCases: int):
        tests = []

        for i in range(numberOfTestCases):
            case = {
                "name": f"test {i}",
                "description": "",
                "max_points": maxPoints,
                "points": actualPoints,
            }

            tests.append(case)

        return tests

    def test50Percent(self):
        results = {
            "tests": self.generateTestResults(10, 5, 100)
        }

        prairieLearnResultFinalizer(results)

        self.assertEqual(results["score"], .5)
        self.assertTrue(results["gradable"])

    def test100Percent(self):
        results = {
            "tests": self.generateTestResults(10, 10, 100)
        }

        prairieLearnResultFinalizer(results)

        self.assertEqual(results["score"], 1)
        self.assertTrue(results["gradable"])

    def testOver100Percent(self):
        results = {
            "tests": self.generateTestResults(10, 100, 100)
        }

        prairieLearnResultFinalizer(results)

        self.assertEqual(results["score"], 1)
        self.assertTrue(results["gradable"])

    def testInvalidTestResults(self):
        results = {
            "tests": [{}]
        }

        prairieLearnResultFinalizer(results)

        self.assertFalse(results["gradable"])

    def testNoTestCases(self):
        results = {
            "tests": []
        }

        prairieLearnResultFinalizer(results)

        self.assertNotIn("score", results)

        self.assertFalse(results["gradable"])

    def testDropUnneededColumns(self):
        results = {
            "tests": self.generateTestResults(10, 10, 1),
            "leaderboard": [],
            "visibility": "visible",
            "stdout_visibility": False,
            "execution_time": .03
        }

        prairieLearnResultFinalizer(results)

        self.assertNotIn("leaderboard", results)
        self.assertNotIn("visibility", results)
        self.assertNotIn("stdout_visibility", results)
        self.assertNotIn("execution_time", results)

        self.assertEqual(results["score"], 1)
        self.assertTrue(results["gradable"])

