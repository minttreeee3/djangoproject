# Generated by Django 4.2.4 on 2023-08-14 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naverdata',
            name='specific_id',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
