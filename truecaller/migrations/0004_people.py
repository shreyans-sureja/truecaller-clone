# Generated by Django 3.0.7 on 2020-06-06 04:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('truecaller', '0003_auto_20200606_0309'),
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, primary_key=True, region=None, serialize=False)),
                ('spam', models.BooleanField(default=False)),
            ],
        ),
    ]