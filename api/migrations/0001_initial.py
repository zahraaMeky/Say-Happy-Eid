# Generated by Django 3.2.8 on 2022-06-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaveImagePath',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=500)),
                ('saveDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
