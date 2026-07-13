from django.test import TestCase
"""Tests for test_10."""

class TestSuite10(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 10, 11)
