from django.test import TestCase

class Suite253(TestCase):
    def test_identity(self):
        self.assertEqual(253, 253)
