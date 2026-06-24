from django.test import TestCase

class TestSuite91(TestCase):
    def test_trivial(self):
        self.assertTrue(91 > 0 and 91 < 200)
