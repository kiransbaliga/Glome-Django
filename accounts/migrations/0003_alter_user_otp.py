# Generated by Django 4.0.4 on 2022-05-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_email_verified_user_otp_user_otp_generated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
