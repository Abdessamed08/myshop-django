#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# This part is added to help Python find the installed packages
# when the environment path is not set up correctly.
site_packages_path = r'C:\Users\AL-Athir Computer\AppData\Local\Programs\Python\Python312\Lib\site-packages'
if site_packages_path not in sys.path:
    sys.path.append(site_packages_path)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()