from django.test import TestCase

class Suite246(TestCase):
    def test_identity(self):
        self.assertEqual(246, 246)
