from django.test import TestCase

class TestSuite95(TestCase):
    def test_trivial(self):
        self.assertTrue(95 > 0 and 95 < 200)
