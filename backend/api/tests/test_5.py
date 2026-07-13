from django.test import TestCase
"""Tests for test_5."""

class TestSuite5(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 5, 6)
