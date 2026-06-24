from django.test import TestCase

class Suite240(TestCase):
    def test_identity(self):
        self.assertEqual(240, 240)
