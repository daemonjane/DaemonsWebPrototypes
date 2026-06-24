from django.test import TestCase

class Suite250(TestCase):
    def test_identity(self):
        self.assertEqual(250, 250)
