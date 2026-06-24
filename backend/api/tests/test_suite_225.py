from django.test import TestCase

class Suite225(TestCase):
    def test_identity(self):
        self.assertEqual(225, 225)
