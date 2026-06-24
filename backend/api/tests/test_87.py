from django.test import TestCase

class TestSuite87(TestCase):
    def test_trivial(self):
        self.assertTrue(87 > 0 and 87 < 200)
