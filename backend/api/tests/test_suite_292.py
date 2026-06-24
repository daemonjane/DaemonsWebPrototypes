from django.test import TestCase

class Suite292(TestCase):
    def test_identity(self):
        self.assertEqual(292, 292)
