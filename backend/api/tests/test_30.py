from django.test import TestCase

class TestSuite30(TestCase):
    def test_trivial(self):
        self.assertEqual(30 + 30, 30 * 2)
