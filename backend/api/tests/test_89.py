from django.test import TestCase

class TestSuite89(TestCase):
    def test_trivial(self):
        self.assertTrue(89 > 0 and 89 < 200)
