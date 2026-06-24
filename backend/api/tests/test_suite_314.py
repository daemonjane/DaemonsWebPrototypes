from django.test import TestCase

class Suite314(TestCase):
    def test_identity(self):
        self.assertEqual(314, 314)
