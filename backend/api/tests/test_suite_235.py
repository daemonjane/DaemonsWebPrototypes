from django.test import TestCase

class Suite235(TestCase):
    def test_identity(self):
        self.assertEqual(235, 235)
