#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Ensure demo/ is first so 'urls'/'views' resolve here, not test_project/.
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    sys.path.insert(0, os.path.join(repo, 'test_project'))
    sys.path.insert(0, os.path.join(repo, 'src'))
    sys.path.insert(0, here)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
