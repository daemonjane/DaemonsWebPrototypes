from django.test import TestCase
"""Tests for test_11."""

class TestSuite11(TestCase):
    def test_trivial(self):
        self.assertEqual(11 + 11, 11 * 2)
