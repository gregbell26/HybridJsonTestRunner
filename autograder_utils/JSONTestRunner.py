import sys
import time
import json
from unittest.signals import registerResult

from autograder_utils.JSONTestResult import JSONTestResult
from autograder_utils.ResultBuilders import gradescopeResultBuilder
from autograder_utils.ResultFinalizers import gradescopeResultFinalizer


class JSONTestRunner(object):
    """A test runner class that displays results in JSON form.
    """
    resultclass = JSONTestResult

    def __init__(self, stream=sys.stdout, descriptions=True, verbosity=1,
                 failfast=False, buffer=True, visibility=None,
                 stdout_visibility=None, post_processor=None,
                 failure_prefix="Test Failed: ", result_builder=gradescopeResultBuilder, result_finalizer=gradescopeResultFinalizer):
        """
        Set buffer to True to include test output in JSON


        post_processor: if supplied, will be called with the final JSON
        data before it is written, allowing the caller to overwrite the
        test results (e.g. add a late penalty) by editing the results
        dict in the first argument.

        failure_prefix: prepended to the output of each test's json
        """
        self.stream = stream
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.post_processor = post_processor
        self.json_data = {
            "tests": [],
            "leaderboard": [],
        }
        if visibility:
            self.json_data["visibility"] = visibility
        if stdout_visibility:
            self.json_data["stdout_visibility"] = stdout_visibility
        self.failure_prefix = failure_prefix
        self.result_builder = result_builder
        self.result_finalizer = result_finalizer

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity,
                                self.json_data["tests"], self.json_data["leaderboard"],
                                self.failure_prefix, self.result_builder)

    def run(self, test):
        """Run the given test case or test suite."""
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime

        self.json_data["execution_time"] = format(timeTaken, "0.2f")

        self.result_finalizer(self.json_data)

        if self.post_processor is not None:
            self.post_processor(self.json_data)

        json.dump(self.json_data, self.stream, indent=4)
        self.stream.write('\n')
        return result
