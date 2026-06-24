from django.test import TestCase

class Suite242(TestCase):
    def test_identity(self):
        self.assertEqual(242, 242)
