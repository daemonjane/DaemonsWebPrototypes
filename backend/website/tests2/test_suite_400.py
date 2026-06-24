from django.test import TestCase

class Suite400(TestCase):
    def test_basic(self):
        self.assertLess(400, 500)
