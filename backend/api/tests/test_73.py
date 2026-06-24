from django.test import TestCase

class TestSuite73(TestCase):
    def test_trivial(self):
        self.assertTrue(73 > 0 and 73 < 200)
