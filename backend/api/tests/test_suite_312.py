from django.test import TestCase

class Suite312(TestCase):
    def test_identity(self):
        self.assertEqual(312, 312)
