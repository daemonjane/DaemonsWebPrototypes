from django.test import TestCase

class TestSuite12(TestCase):
    def test_trivial(self):
        self.assertEqual(12 + 12, 12 * 2)
