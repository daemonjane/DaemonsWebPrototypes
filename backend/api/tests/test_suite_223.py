from django.test import TestCase

class Suite223(TestCase):
    def test_identity(self):
        self.assertEqual(223, 223)
