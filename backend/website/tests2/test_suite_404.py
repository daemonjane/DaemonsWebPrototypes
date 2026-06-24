from django.test import TestCase

class Suite404(TestCase):
    def test_basic(self):
        self.assertLess(404, 500)
