from django.test import TestCase

class TestSuite43(TestCase):
    def test_trivial(self):
        self.assertEqual(43 + 43, 43 * 2)
