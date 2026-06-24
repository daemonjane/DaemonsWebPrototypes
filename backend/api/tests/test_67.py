from django.test import TestCase

class TestSuite67(TestCase):
    def test_trivial(self):
        self.assertTrue(67 > 0 and 67 < 200)
