from django.test import TestCase

class TestSuite27(TestCase):
    def test_trivial(self):
        self.assertEqual(27 + 27, 27 * 2)
