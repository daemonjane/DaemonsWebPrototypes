from django.test import TestCase

class Suite304(TestCase):
    def test_identity(self):
        self.assertEqual(304, 304)
