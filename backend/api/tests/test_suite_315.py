from django.test import TestCase

class Suite315(TestCase):
    def test_identity(self):
        self.assertEqual(315, 315)
