from django.test import TestCase

class Suite389(TestCase):
    def test_basic(self):
        self.assertLess(389, 500)
