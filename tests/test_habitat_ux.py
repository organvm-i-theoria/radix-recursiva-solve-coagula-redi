import unittest
import sys
import io
import time
from habitat_ux import Spinner, Colors

class TestHabitatUX(unittest.TestCase):

    def test_spinner_output(self):
        """Test that spinner writes to stdout and cleans up."""
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            with Spinner("Testing...", delay=0.01):
                time.sleep(0.05)
        finally:
            sys.stdout = original_stdout

        output = captured_output.getvalue()

        # Should contain spinner frames
        self.assertIn("⠋", output)
        self.assertIn("Testing...", output)
        # Should contain ANSI colors
        self.assertIn(Colors.CYAN, output)
        # Should contain carriage returns
        self.assertIn("\r", output)

    def test_colors_exist(self):
        """Test that Colors class has expected attributes."""
        self.assertTrue(hasattr(Colors, 'HEADER'))
        self.assertTrue(hasattr(Colors, 'BLUE'))
        self.assertTrue(hasattr(Colors, 'CYAN'))
        self.assertTrue(hasattr(Colors, 'GREEN'))
        self.assertTrue(hasattr(Colors, 'YELLOW'))
        self.assertTrue(hasattr(Colors, 'RED'))
        self.assertTrue(hasattr(Colors, 'RESET'))
        self.assertTrue(hasattr(Colors, 'BOLD'))
        self.assertTrue(hasattr(Colors, 'UNDERLINE'))

if __name__ == '__main__':
    unittest.main()
