from django.test import TestCase

class TestSuite4(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 4, 1)
