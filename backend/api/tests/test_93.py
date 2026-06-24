from django.test import TestCase

class TestSuite93(TestCase):
    def test_trivial(self):
        self.assertTrue(93 > 0 and 93 < 200)
