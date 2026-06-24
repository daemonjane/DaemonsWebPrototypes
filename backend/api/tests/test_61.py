from django.test import TestCase

class TestSuite61(TestCase):
    def test_trivial(self):
        self.assertTrue(61 > 0 and 61 < 200)
