from django.test import TestCase

class TestSuite79(TestCase):
    def test_trivial(self):
        self.assertTrue(79 > 0 and 79 < 200)
