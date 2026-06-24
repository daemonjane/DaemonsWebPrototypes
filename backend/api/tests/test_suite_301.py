from django.test import TestCase

class Suite301(TestCase):
    def test_identity(self):
        self.assertEqual(301, 301)
