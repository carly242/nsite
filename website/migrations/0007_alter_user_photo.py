# Generated by Django 5.0.4 on 2024-05-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_user_email_bureau_alter_user_office_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/photos/'),
        ),
    ]
