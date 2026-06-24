from django.test import TestCase

class Suite303(TestCase):
    def test_identity(self):
        self.assertEqual(303, 303)
