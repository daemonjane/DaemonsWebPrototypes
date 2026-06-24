from django.test import TestCase

class Suite309(TestCase):
    def test_identity(self):
        self.assertEqual(309, 309)
