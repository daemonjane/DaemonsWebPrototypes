from django.test import TestCase

class TestSuite99(TestCase):
    def test_trivial(self):
        self.assertTrue(99 > 0 and 99 < 200)
