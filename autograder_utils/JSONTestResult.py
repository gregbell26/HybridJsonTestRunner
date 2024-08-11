import abc
from unittest import result


class JSONTestResult(result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by JSONTestRunner.
    """

    def __init__(self, stream, descriptions, verbosity, results, leaderboard,
                 failure_prefix, build_results):
        super(JSONTestResult, self).__init__(stream, descriptions, verbosity)
        self.descriptions = descriptions
        self.results = results
        self.leaderboard = leaderboard
        self.failure_prefix = failure_prefix
        self.build_result = build_results

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def getTestMethodName(self, test):
        if "_testMethodName" not in vars(test):
            return None

        return getattr(test, test._testMethodName)

    def getTags(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__tags__', None)

    def getWeight(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__weight__', None)

    def getScore(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__score__', None)

    def getNumber(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__number__', None)

    def getVisibility(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__visibility__', None)

    def getHideErrors(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        return getattr(testMethodName, '__hide_errors__', None)

    def getLeaderboardData(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None, None, None

        column_name = getattr(testMethodName, '__leaderboard_column__', None)
        sort_order = getattr(testMethodName, '__leaderboard_sort_order__', None)
        value = getattr(testMethodName, '__leaderboard_value__', None)
        return column_name, sort_order, value


    def getImageData(self, test):
        testMethodName = self.getTestMethodName(test)

        if not testMethodName:
            return None

        image_data = getattr(testMethodName, "__image_data__", None)
        return image_data

    def startTest(self, test):
        super(JSONTestResult, self).startTest(test)

    def getOutput(self):
        if self.buffer:
            out = self._stdout_buffer.getvalue()
            err = self._stderr_buffer.getvalue()
            if err:
                if not out.endswith('\n'):
                    out += '\n'
                out += err
            return out

    def buildResult(self, test, err=None):
        failed = err is not None
        weight = self.getWeight(test)
        tags = self.getTags(test)
        number = self.getNumber(test)
        visibility = self.getVisibility(test)
        hide_errors_message = self.getHideErrors(test)
        score = self.getScore(test)
        output = self.getOutput() or ""
        name = self.getDescription(test)
        image_data = self.getImageData(test)

        return self.build_result(name, self.failure_prefix, err, hide_errors_message, weight, tags, number, visibility, score, output, image_data)

    def buildLeaderboardEntry(self, test):
        name, sort_order, value = self.getLeaderboardData(test)
        return {
            "name": name,
            "value": value,
            "order": sort_order,
        }

    def processResult(self, test, err=None):
        if self.getLeaderboardData(test)[0]:
            self.leaderboard.append(self.buildLeaderboardEntry(test))
        else:
            self.results.append(self.buildResult(test, err))

    def addSuccess(self, test):
        super(JSONTestResult, self).addSuccess(test)
        self.processResult(test)

    def addError(self, test, err):
        super(JSONTestResult, self).addError(test, err)
        # Prevent output from being printed to stdout on failure
        self._mirrorOutput = False
        self.processResult(test, err)

    def addFailure(self, test, err):
        super(JSONTestResult, self).addFailure(test, err)
        self._mirrorOutput = False
        self.processResult(test, err)
