from django.test import TestCase

class Suite241(TestCase):
    def test_identity(self):
        self.assertEqual(241, 241)
