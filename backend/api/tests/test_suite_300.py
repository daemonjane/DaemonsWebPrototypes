from django.test import TestCase

class Suite300(TestCase):
    def test_identity(self):
        self.assertEqual(300, 300)
