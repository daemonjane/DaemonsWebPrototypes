from django.test import TestCase

class TestSuite115(TestCase):
    def test_trivial(self):
        self.assertTrue(115 > 0 and 115 < 200)
