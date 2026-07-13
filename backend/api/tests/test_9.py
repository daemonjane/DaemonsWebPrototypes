from django.test import TestCase
"""Tests for test_9."""

class TestSuite9(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 9, 10)
