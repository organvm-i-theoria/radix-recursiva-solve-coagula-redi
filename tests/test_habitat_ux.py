#!/usr/bin/env python3
"""
TEST_HABITAT_UX.py

Unit tests for habitat_ux utilities.
"""

import unittest
import sys
import os
import time
from io import StringIO
from unittest.mock import patch

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import habitat_ux

class TestSpinner(unittest.TestCase):
    """Test Spinner class"""

    def test_spinner_context_manager(self):
        """Test that Spinner works as a context manager"""
        # We verify that it doesn't crash and prints something
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with habitat_ux.Spinner("Testing..."):
                time.sleep(0.1)

            output = fake_out.getvalue()
            # It should have printed the message and some spinner characters
            self.assertIn("Testing...", output)
            # It should have cleaned up the line
            self.assertIn("\r", output)

    def test_spinner_manual_start_stop(self):
        """Test manual start and stop of Spinner"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            spinner = habitat_ux.Spinner("Manual test")
            spinner.start()
            time.sleep(0.1)
            spinner.stop()

            output = fake_out.getvalue()
            self.assertIn("Manual test", output)

if __name__ == "__main__":
    unittest.main()
