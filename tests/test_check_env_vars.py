import unittest
import os
import subprocess
import sys

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCheckEnvVars(unittest.TestCase):

    def test_missing_env_vars(self):
        """
        Test that the script exits with a non-zero status code when env vars are missing.
        """
        env = os.environ.copy()
        if "API_KEY" in env:
            del env["API_KEY"]
        if "DATABASE_URL" in env:
            del env["DATABASE_URL"]

        process = subprocess.run(
            [sys.executable, "scripts/check_env_vars.py"],
            capture_output=True,
            text=True,
            env=env
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("Missing required environment variables", process.stderr)

    def test_all_env_vars_present(self):
        """
        Test that the script exits with a zero status code when all env vars are present.
        """
        env = os.environ.copy()
        env["API_KEY"] = "test_key"
        env["DATABASE_URL"] = "test_url"

        process = subprocess.run(
            [sys.executable, "scripts/check_env_vars.py"],
            capture_output=True,
            text=True,
            env=env
        )
        self.assertEqual(process.returncode, 0)
        self.assertIn("All required environment variables are set.", process.stdout)

if __name__ == "__main__":
    unittest.main()
