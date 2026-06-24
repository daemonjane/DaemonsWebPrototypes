from django.test import TestCase

class Suite293(TestCase):
    def test_identity(self):
        self.assertEqual(293, 293)
