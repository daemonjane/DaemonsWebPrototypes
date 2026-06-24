from django.test import TestCase

class Suite261(TestCase):
    def test_identity(self):
        self.assertEqual(261, 261)
