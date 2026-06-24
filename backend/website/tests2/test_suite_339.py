from django.test import TestCase

class Suite339(TestCase):
    def test_basic(self):
        self.assertLess(339, 500)
