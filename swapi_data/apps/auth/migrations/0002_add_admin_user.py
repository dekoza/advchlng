from decouple import config
from django.contrib.auth import get_user_model
from django.db import migrations

DEFAULT_SUPERUSER_USERNAME = config("DEFAULT_SUPERUSER_USERNAME", default="admin")
DEFAULT_SUPERUSER_PASSWORD = config("DEFAULT_SUPERUSER_PASSWORD", default="admin")


def create_superuser(apps, schema_editor):
    User = get_user_model()
    User.objects.create_superuser(
        username=DEFAULT_SUPERUSER_USERNAME,
        password=DEFAULT_SUPERUSER_PASSWORD,
        first_name="Default",
        last_name="Admin",
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [("auth", "0001_initial")]

    operations = [
        migrations.RunPython(create_superuser)
    ]
