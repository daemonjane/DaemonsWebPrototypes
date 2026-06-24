from django.test import TestCase

class TestSuite63(TestCase):
    def test_trivial(self):
        self.assertTrue(63 > 0 and 63 < 200)
