import unittest

from components import capture, comparison, recognition

class TestComponents(unittest.TestCase):
    def setUp(self):
        self.capture = capture.Capture()
        self.comparison = comparison.Comparison()
        self.recognition = recognition.Recognition()

    def test_capture(self):
        self.assertIsNotNone(self.capture)

    def test_comparison(self):
        self.assertIsNotNone(self.comparison)

    def test_recognition(self):
        self.assertIsNotNone(self.recognition)

    def tearDown(self):
        self.capture = None
        self.comparison = None
        self.recognition = None