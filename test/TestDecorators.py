import unittest

# import matplotlib.pyplot as plt

from autograder_utils.Decorators import Weight, Number, Visibility, HideErrors, Tags, Leaderboard, ImageResult, \
    PartialCredit, OutputMessage


class TestDecorators(unittest.TestCase):

    @Weight(10)
    def testVerifyWeight(self):
        weightAttr = getattr(self.testVerifyWeight, "__weight__", None)

        self.assertIsNotNone(weightAttr)

        self.assertEqual(10, weightAttr)

    @Number(1.0)
    def testVerifyNumber(self):
        numberAttr = getattr(self.testVerifyNumber, "__number__", None)

        self.assertIsNotNone(numberAttr)

        self.assertEqual("1.0", numberAttr)

    @Visibility("hidden")
    def testVerifyVisibility(self):
        visAttr = getattr(self.testVerifyVisibility, "__visibility__", None)

        self.assertIsNotNone(visAttr)

        self.assertEqual("hidden", visAttr)

    @HideErrors()
    def testVerifyHideErrorsDefault(self):
        hideErrorsAttr = getattr(self.testVerifyHideErrorsDefault, "__hide_errors__", None)

        self.assertIsNotNone(hideErrorsAttr)

        self.assertEqual("Test failed", hideErrorsAttr)

    @HideErrors("Yo test failed dawg")
    def testVerifyHideErrorsCustomError(self):
        hideErrorsAttr = getattr(self.testVerifyHideErrorsCustomError, "__hide_errors__", None)

        self.assertIsNotNone(hideErrorsAttr)

        self.assertEqual("Yo test failed dawg", hideErrorsAttr)

    @Tags("c1", "c2")
    def testVerifyConceptTags(self):
        tagsAttr = getattr(self.testVerifyConceptTags, "__tags__", None)

        self.assertIsNotNone(tagsAttr)

        self.assertCountEqual(["c1", "c2"], tagsAttr)

    @Leaderboard("points")
    def testVerifyLeaderboard(self, set_leaderboard_value=None):
        expected = 100
        self.assertIsNotNone(set_leaderboard_value)

        set_leaderboard_value(expected)

        leaderboardAttr = getattr(self.testVerifyLeaderboard, "__leaderboard_value__", None)

        self.assertIsNotNone(leaderboardAttr)

        self.assertEqual(expected, leaderboardAttr)

    @ImageResult()
    @unittest.skip("API change")
    def testVerifyImageResult(self, load_data, set_data):
        self.assertIsNotNone(load_data)
        self.assertIsNotNone(set_data)

        plt.plot([1, 2, 3], [2, 3, 0])
        plt.savefig("plot.png")

        data = load_data("plot.png")

        set_data("test_plot", data)

        dataAttr = getattr(self.testVerifyImageResult, "__image_data__", None)

        self.assertDictEqual({"label": "test_plot", "data": data, "image_type": "png"}, dataAttr)

    @PartialCredit(100)
    def testVerifyPartialCredit(self, set_score=None):
        expected = 10
        self.assertIsNotNone(set_score)

        set_score(expected)

        scoreAttr = getattr(self.testVerifyPartialCredit, "__score__", None)

        self.assertIsNotNone(scoreAttr)
        self.assertEqual(expected, scoreAttr)


    @PartialCredit(100)
    def testVerifyPartialCredit(self, set_score=None):
        expected = 10
        self.assertIsNotNone(set_score)

        set_score(expected)

        scoreAttr = getattr(self.testVerifyPartialCredit, "__score__", None)

        self.assertIsNotNone(scoreAttr)
        self.assertEqual(expected, scoreAttr)

    @OutputMessage()
    def testVerifyOutputMessage(self, set_output=None):
        expected = "huzzah"
        self.assertIsNotNone(set_output)

        set_output(expected)

        outputAttr = getattr(self.testVerifyOutputMessage, "__output__", None)

        self.assertIsNotNone(outputAttr)
        self.assertEqual(expected, outputAttr)

    def testVerifyStackedDecorators(self):
        expectedScore = 10
        expectedMessage = "Huzzah"

        @PartialCredit(10)
        @OutputMessage()
        def runTestMethod(set_score=None, set_output=None):
            self.assertIsNotNone(set_score)
            self.assertIsNotNone(set_output)


            set_score(expectedScore)
            set_output(expectedMessage)

        runTestMethod()

        scoreAttr = getattr(runTestMethod, "__score__", None)
        outputAttr = getattr(runTestMethod, "__output__", None)



        self.assertIsNotNone(scoreAttr)
        self.assertIsNotNone(outputAttr)

        self.assertEqual(expectedScore, scoreAttr)
        self.assertEqual(expectedMessage, outputAttr)

