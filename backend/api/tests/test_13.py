from django.test import TestCase
"""Tests for test_13."""

class TestSuite13(TestCase):
    def test_trivial(self):
        self.assertEqual(13 + 13, 13 * 2)
