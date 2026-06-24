from django.test import TestCase

class Suite285(TestCase):
    def test_identity(self):
        self.assertEqual(285, 285)
