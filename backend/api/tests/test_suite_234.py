from django.test import TestCase

class Suite234(TestCase):
    def test_identity(self):
        self.assertEqual(234, 234)
