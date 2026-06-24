from django.test import TestCase

class Suite262(TestCase):
    def test_identity(self):
        self.assertEqual(262, 262)
