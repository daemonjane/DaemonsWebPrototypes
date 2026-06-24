from django.test import TestCase

class TestSuite85(TestCase):
    def test_trivial(self):
        self.assertTrue(85 > 0 and 85 < 200)
