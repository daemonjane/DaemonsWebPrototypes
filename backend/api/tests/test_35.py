from django.test import TestCase

class TestSuite35(TestCase):
    def test_trivial(self):
        self.assertEqual(35 + 35, 35 * 2)
