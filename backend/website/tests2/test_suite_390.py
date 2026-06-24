from django.test import TestCase

class Suite390(TestCase):
    def test_basic(self):
        self.assertLess(390, 500)
