from django.test import TestCase

class TestSuite65(TestCase):
    def test_trivial(self):
        self.assertTrue(65 > 0 and 65 < 200)
