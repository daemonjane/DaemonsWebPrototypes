from django.test import TestCase

class Suite308(TestCase):
    def test_identity(self):
        self.assertEqual(308, 308)
