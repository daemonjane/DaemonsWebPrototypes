from django.test import TestCase

class Suite233(TestCase):
    def test_identity(self):
        self.assertEqual(233, 233)
