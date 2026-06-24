from django.test import TestCase

class TestSuite110(TestCase):
    def test_trivial(self):
        self.assertTrue(110 > 0 and 110 < 200)
