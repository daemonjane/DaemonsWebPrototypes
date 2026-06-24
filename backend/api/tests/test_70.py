from django.test import TestCase

class TestSuite70(TestCase):
    def test_trivial(self):
        self.assertTrue(70 > 0 and 70 < 200)
