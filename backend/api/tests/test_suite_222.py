from django.test import TestCase

class Suite222(TestCase):
    def test_identity(self):
        self.assertEqual(222, 222)
