from django.test import TestCase

class TestSuite7(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 7, 1)
