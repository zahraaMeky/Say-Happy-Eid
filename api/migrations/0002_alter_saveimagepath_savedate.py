# Generated by Django 3.2.8 on 2022-06-28 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveimagepath',
            name='saveDate',
            field=models.DateTimeField(),
        ),
    ]
