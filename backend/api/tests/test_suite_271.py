from django.test import TestCase

class Suite271(TestCase):
    def test_identity(self):
        self.assertEqual(271, 271)
