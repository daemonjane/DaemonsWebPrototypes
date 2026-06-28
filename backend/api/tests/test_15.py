from django.test import TestCase
"""Tests for test_15."""

class TestSuite15(TestCase):
    def test_trivial(self):
        self.assertEqual(15 + 15, 15 * 2)
