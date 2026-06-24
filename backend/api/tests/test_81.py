from django.test import TestCase

class TestSuite81(TestCase):
    def test_trivial(self):
        self.assertTrue(81 > 0 and 81 < 200)
