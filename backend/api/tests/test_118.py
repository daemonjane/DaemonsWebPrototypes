from django.test import TestCase

class TestSuite118(TestCase):
    def test_trivial(self):
        self.assertTrue(118 > 0 and 118 < 200)
