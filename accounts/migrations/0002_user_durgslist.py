# Generated by Django 4.2.6 on 2023-10-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drugs", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="durgslist",
            field=models.ManyToManyField(
                blank=True, related_name="takers", to="drugs.drug"
            ),
        ),
    ]
