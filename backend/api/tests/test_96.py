from django.test import TestCase

class TestSuite96(TestCase):
    def test_trivial(self):
        self.assertTrue(96 > 0 and 96 < 200)
