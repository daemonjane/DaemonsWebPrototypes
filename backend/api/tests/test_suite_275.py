from django.test import TestCase

class Suite275(TestCase):
    def test_identity(self):
        self.assertEqual(275, 275)
