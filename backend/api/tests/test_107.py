from django.test import TestCase

class TestSuite107(TestCase):
    def test_trivial(self):
        self.assertTrue(107 > 0 and 107 < 200)
