from django.test import TestCase

class TestSuite97(TestCase):
    def test_trivial(self):
        self.assertTrue(97 > 0 and 97 < 200)
