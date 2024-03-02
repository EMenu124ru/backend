#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.development")

    from django.core.management import execute_from_command_line

    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "apps"))

    execute_from_command_line(sys.argv)
