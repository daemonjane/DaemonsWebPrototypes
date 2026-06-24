from django.test import TestCase

class Suite299(TestCase):
    def test_identity(self):
        self.assertEqual(299, 299)
