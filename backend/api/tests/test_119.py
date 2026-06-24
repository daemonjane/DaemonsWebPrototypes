from django.test import TestCase

class TestSuite119(TestCase):
    def test_trivial(self):
        self.assertTrue(119 > 0 and 119 < 200)
