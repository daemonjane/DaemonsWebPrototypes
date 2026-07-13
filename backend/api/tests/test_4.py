from django.test import TestCase
"""Tests for test_4."""

class TestSuite4(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 4, 5)
