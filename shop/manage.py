#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
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



######################### auth Client id and scerect  #################@@@@@@@@@@#############@@@@@@@@@@###########@@@@@@@@@@@@

#Client_Id = 97886935153-odbe7jic5mau74is27vs6lm7qgnbc3nr.apps.googleusercontent.com

#Client_secret = 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

# twilio pass = pj_!GTTzm4W#MQZ

# recovery code = GTYTRG7G1RKTJRLTEUBBAVE2
