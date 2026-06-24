from django.test import TestCase

class TestSuite80(TestCase):
    def test_trivial(self):
        self.assertTrue(80 > 0 and 80 < 200)
