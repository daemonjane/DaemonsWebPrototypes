from django.test import TestCase
"""Tests for test_6."""

class TestSuite6(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 6, 7)
