from django.test import TestCase
"""Tests for test_12."""

class TestSuite12(TestCase):
    def test_trivial(self):
        self.assertEqual(12 + 12, 12 * 2)
