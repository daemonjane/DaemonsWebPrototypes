from django.test import TestCase

class Suite260(TestCase):
    def test_identity(self):
        self.assertEqual(260, 260)
