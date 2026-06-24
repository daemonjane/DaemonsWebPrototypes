from django.test import TestCase

class TestSuite120(TestCase):
    def test_trivial(self):
        self.assertTrue(120 > 0 and 120 < 200)
