from django.test import TestCase
"""Tests for test_8."""

class TestSuite8(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 8, 9)
