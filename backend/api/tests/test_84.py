from django.test import TestCase

class TestSuite84(TestCase):
    def test_trivial(self):
        self.assertTrue(84 > 0 and 84 < 200)
