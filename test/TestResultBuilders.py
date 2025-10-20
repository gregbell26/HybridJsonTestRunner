import unittest

from autograder_utils.ResultBuilders import gradescopeResultBuilder, prairieLearnResultBuilder

class VerifyGradescopeResults(unittest.TestCase):
    def testImageIsHTMLEncoded(self):
        res = gradescopeResultBuilder("test", None, None, None, 1.0, None, "1.0", None, 1.0, None, {
            "image_type": "png",
            "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0lEQVR4AQEEAPv/APhl5QSbAkNZHEs8AAAAAElFTkSuQmCC",
            "label": "A pink square",
        }, "html")

        self.assertIsNotNone(res["output"])
        self.assertIn("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0lEQVR4AQEEAPv/APhl5QSbAkNZHEs8AAAAAElFTkSuQmCC", res["output"])
        self.assertEqual("html", res["output_format"])

class VerifyPrairielearnResults(unittest.TestCase):
    def testImageIsHTMLEncoded(self):
        res = prairieLearnResultBuilder("test", None, None, None, 1.0, None, "1.0", None, 1.0, None, {
            "image_type": "png",
            "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0lEQVR4AQEEAPv/APhl5QSbAkNZHEs8AAAAAElFTkSuQmCC",
            "label": "A pink square",
        }, "html")

        self.assertIsNotNone(res["images"])
        self.assertEqual("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0lEQVR4AQEEAPv/APhl5QSbAkNZHEs8AAAAAElFTkSuQmCC", res["images"]["url"])
