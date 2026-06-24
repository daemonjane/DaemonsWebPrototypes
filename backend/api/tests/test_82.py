from django.test import TestCase

class TestSuite82(TestCase):
    def test_trivial(self):
        self.assertTrue(82 > 0 and 82 < 200)
