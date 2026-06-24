from django.test import TestCase

class TestSuite94(TestCase):
    def test_trivial(self):
        self.assertTrue(94 > 0 and 94 < 200)
