from django.test import TestCase

class TestSuite83(TestCase):
    def test_trivial(self):
        self.assertTrue(83 > 0 and 83 < 200)
