from django.test import TestCase

class TestSuite68(TestCase):
    def test_trivial(self):
        self.assertTrue(68 > 0 and 68 < 200)
