from django.test import TestCase

class Suite251(TestCase):
    def test_identity(self):
        self.assertEqual(251, 251)
