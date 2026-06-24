from django.test import TestCase

class Suite283(TestCase):
    def test_identity(self):
        self.assertEqual(283, 283)
