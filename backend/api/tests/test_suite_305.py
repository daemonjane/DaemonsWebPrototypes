from django.test import TestCase

class Suite305(TestCase):
    def test_identity(self):
        self.assertEqual(305, 305)
