import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.utils import timezone

print("UTC:", timezone.now())
print("VN :", timezone.localtime())
print("TZ :", timezone.get_current_timezone_name())