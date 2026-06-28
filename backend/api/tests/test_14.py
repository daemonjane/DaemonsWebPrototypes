from django.test import TestCase
"""Tests for test_14."""

class TestSuite14(TestCase):
    def test_trivial(self):
        self.assertEqual(14 + 14, 14 * 2)
