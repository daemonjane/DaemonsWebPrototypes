from django.test import TestCase

class Suite298(TestCase):
    def test_identity(self):
        self.assertEqual(298, 298)
