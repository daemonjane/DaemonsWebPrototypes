from django.test import TestCase

class Suite289(TestCase):
    def test_identity(self):
        self.assertEqual(289, 289)
