from django.test import TestCase

class Suite255(TestCase):
    def test_identity(self):
        self.assertEqual(255, 255)
