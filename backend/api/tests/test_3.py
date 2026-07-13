from django.test import TestCase
"""Tests for test_3."""

class TestSuite3(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 3, 4)
