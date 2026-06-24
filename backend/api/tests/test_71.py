from django.test import TestCase

class TestSuite71(TestCase):
    def test_trivial(self):
        self.assertTrue(71 > 0 and 71 < 200)
