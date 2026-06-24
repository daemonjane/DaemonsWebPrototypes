from django.test import TestCase

class TestSuite62(TestCase):
    def test_trivial(self):
        self.assertTrue(62 > 0 and 62 < 200)
