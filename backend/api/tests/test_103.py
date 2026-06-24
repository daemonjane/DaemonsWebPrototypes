from django.test import TestCase

class TestSuite103(TestCase):
    def test_trivial(self):
        self.assertTrue(103 > 0 and 103 < 200)
