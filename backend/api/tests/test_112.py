from django.test import TestCase

class TestSuite112(TestCase):
    def test_trivial(self):
        self.assertTrue(112 > 0 and 112 < 200)
