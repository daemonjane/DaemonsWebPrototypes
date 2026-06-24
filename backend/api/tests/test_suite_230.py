from django.test import TestCase

class Suite230(TestCase):
    def test_identity(self):
        self.assertEqual(230, 230)
