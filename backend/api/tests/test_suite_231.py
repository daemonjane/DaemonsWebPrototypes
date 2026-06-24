from django.test import TestCase

class Suite231(TestCase):
    def test_identity(self):
        self.assertEqual(231, 231)
