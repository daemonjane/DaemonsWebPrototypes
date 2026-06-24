from django.test import TestCase

class Suite270(TestCase):
    def test_identity(self):
        self.assertEqual(270, 270)
