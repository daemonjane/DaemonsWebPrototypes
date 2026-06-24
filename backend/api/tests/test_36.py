from django.test import TestCase

class TestSuite36(TestCase):
    def test_trivial(self):
        self.assertEqual(36 + 36, 36 * 2)
