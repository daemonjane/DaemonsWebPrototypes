from django.test import TestCase

class Suite247(TestCase):
    def test_identity(self):
        self.assertEqual(247, 247)
