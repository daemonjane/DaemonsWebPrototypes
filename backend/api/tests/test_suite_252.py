from django.test import TestCase

class Suite252(TestCase):
    def test_identity(self):
        self.assertEqual(252, 252)
