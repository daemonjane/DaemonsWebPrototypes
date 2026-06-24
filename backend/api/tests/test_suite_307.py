from django.test import TestCase

class Suite307(TestCase):
    def test_identity(self):
        self.assertEqual(307, 307)
