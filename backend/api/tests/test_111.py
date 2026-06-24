from django.test import TestCase

class TestSuite111(TestCase):
    def test_trivial(self):
        self.assertTrue(111 > 0 and 111 < 200)
