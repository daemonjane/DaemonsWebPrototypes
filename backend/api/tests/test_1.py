from django.test import TestCase
"""Tests for test_1."""

class TestSuite1(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 1, 1)
