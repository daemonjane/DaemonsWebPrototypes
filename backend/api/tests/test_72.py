from django.test import TestCase

class TestSuite72(TestCase):
    def test_trivial(self):
        self.assertTrue(72 > 0 and 72 < 200)
