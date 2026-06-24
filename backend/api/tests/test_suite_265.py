from django.test import TestCase

class Suite265(TestCase):
    def test_identity(self):
        self.assertEqual(265, 265)
