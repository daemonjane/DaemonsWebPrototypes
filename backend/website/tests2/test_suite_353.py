from django.test import TestCase

class Suite353(TestCase):
    def test_basic(self):
        self.assertLess(353, 500)
