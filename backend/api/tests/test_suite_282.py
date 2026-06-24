from django.test import TestCase

class Suite282(TestCase):
    def test_identity(self):
        self.assertEqual(282, 282)
