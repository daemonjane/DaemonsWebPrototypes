from django.test import TestCase

class Suite313(TestCase):
    def test_identity(self):
        self.assertEqual(313, 313)
