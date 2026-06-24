from django.test import TestCase

class TestSuite75(TestCase):
    def test_trivial(self):
        self.assertTrue(75 > 0 and 75 < 200)
