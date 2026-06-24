from django.test import TestCase

class Suite226(TestCase):
    def test_identity(self):
        self.assertEqual(226, 226)
