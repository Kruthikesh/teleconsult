# Generated by Django 4.1.7 on 2023-04-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doctor_id',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
