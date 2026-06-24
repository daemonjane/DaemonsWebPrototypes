from django.test import TestCase

class Suite232(TestCase):
    def test_identity(self):
        self.assertEqual(232, 232)
