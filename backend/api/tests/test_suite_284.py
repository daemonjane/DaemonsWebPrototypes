from django.test import TestCase

class Suite284(TestCase):
    def test_identity(self):
        self.assertEqual(284, 284)
