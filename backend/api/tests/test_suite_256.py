from django.test import TestCase

class Suite256(TestCase):
    def test_identity(self):
        self.assertEqual(256, 256)
