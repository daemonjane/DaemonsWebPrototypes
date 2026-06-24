from django.test import TestCase

class Suite280(TestCase):
    def test_identity(self):
        self.assertEqual(280, 280)
