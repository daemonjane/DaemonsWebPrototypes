from django.test import TestCase

class TestSuite78(TestCase):
    def test_trivial(self):
        self.assertTrue(78 > 0 and 78 < 200)
