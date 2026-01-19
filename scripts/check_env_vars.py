import os
import sys

REQUIRED_ENV_VARS = [
    "API_KEY",
    "DATABASE_URL"
]

def check_env_vars():
    """
    Checks for the presence of required environment variables.
    Exits with an error if any are missing.
    """
    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}", file=sys.stderr)
        sys.exit(1)
    else:
        print("All required environment variables are set.")

if __name__ == "__main__":
    check_env_vars()
