from django.test import TestCase

class Suite320(TestCase):
    def test_identity(self):
        self.assertEqual(320, 320)
