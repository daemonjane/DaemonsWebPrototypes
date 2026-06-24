from django.test import TestCase

class Suite311(TestCase):
    def test_identity(self):
        self.assertEqual(311, 311)
