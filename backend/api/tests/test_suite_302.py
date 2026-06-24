from django.test import TestCase

class Suite302(TestCase):
    def test_identity(self):
        self.assertEqual(302, 302)
