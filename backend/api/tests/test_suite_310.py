from django.test import TestCase

class Suite310(TestCase):
    def test_identity(self):
        self.assertEqual(310, 310)
