from django.test import TestCase

class TestSuite20(TestCase):
    def test_trivial(self):
        self.assertEqual(20 + 20, 20 * 2)
