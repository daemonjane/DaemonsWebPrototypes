from django.test import TestCase

class TestSuite108(TestCase):
    def test_trivial(self):
        self.assertTrue(108 > 0 and 108 < 200)
