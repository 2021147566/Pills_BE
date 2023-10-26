# Generated by Django 4.2.6 on 2023-10-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('drug_image', models.ImageField(blank=True, null=True, upload_to='media/drugImg')),
                ('form', models.CharField(max_length=100)),
                ('ingredient', models.TextField(max_length=200)),
            ],
        ),
    ]
