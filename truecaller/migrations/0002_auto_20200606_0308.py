# Generated by Django 3.0.7 on 2020-06-06 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truecaller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerusers',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
