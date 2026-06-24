from django.test import TestCase

class TestSuite69(TestCase):
    def test_trivial(self):
        self.assertTrue(69 > 0 and 69 < 200)
