from django.test import TestCase
"""Tests for test_7."""

class TestSuite7(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 7, 1)
