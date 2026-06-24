from django.test import TestCase

class TestSuite102(TestCase):
    def test_trivial(self):
        self.assertTrue(102 > 0 and 102 < 200)
