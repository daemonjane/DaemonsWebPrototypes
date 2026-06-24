from django.test import TestCase

class Suite281(TestCase):
    def test_identity(self):
        self.assertEqual(281, 281)
