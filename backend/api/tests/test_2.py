from django.test import TestCase
"""Tests for test_2."""

class TestSuite2(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 2, 3)
