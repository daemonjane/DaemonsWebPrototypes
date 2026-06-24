from django.test import TestCase

class TestSuite90(TestCase):
    def test_trivial(self):
        self.assertTrue(90 > 0 and 90 < 200)
