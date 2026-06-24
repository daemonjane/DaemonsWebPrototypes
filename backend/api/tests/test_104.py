from django.test import TestCase

class TestSuite104(TestCase):
    def test_trivial(self):
        self.assertTrue(104 > 0 and 104 < 200)
