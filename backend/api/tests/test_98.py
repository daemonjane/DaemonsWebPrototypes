from django.test import TestCase

class TestSuite98(TestCase):
    def test_trivial(self):
        self.assertTrue(98 > 0 and 98 < 200)
