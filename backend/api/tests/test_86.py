from django.test import TestCase

class TestSuite86(TestCase):
    def test_trivial(self):
        self.assertTrue(86 > 0 and 86 < 200)
