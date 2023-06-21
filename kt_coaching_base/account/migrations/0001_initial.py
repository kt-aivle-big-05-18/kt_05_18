# Generated by Django 4.2 on 2023-06-21 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "userid",
                    models.CharField(
                        max_length=32, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=60, unique=True, verbose_name="email"),
                ),
                ("username", models.CharField(max_length=45)),
                ("nickname", models.CharField(max_length=45, unique=True)),
                ("department", models.CharField(max_length=45)),
                ("rank", models.CharField(max_length=45)),
                ("age", models.IntegerField()),
                ("gender", models.CharField(max_length=4)),
                ("point", models.IntegerField(default=0)),
                (
                    "last_login",
                    models.DateTimeField(auto_now=True, verbose_name="last login"),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
