from django.test import TestCase

class Suite221(TestCase):
    def test_identity(self):
        self.assertEqual(221, 221)
