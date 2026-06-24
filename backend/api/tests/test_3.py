from django.test import TestCase

class TestSuite3(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 3, 1)
