from django.test import TestCase

class TestSuite117(TestCase):
    def test_trivial(self):
        self.assertTrue(117 > 0 and 117 < 200)
