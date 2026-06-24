from django.test import TestCase

class TestSuite88(TestCase):
    def test_trivial(self):
        self.assertTrue(88 > 0 and 88 < 200)
