from django.test import TestCase

class TestSuite116(TestCase):
    def test_trivial(self):
        self.assertTrue(116 > 0 and 116 < 200)
