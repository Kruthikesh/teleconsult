# Generated by Django 4.1.7 on 2023-05-14 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tcd', '0006_rename_patientreviewimages_patientreviewimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorsuggestion',
            name='tcd',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_suggestions', to='tcd.tcd'),
        ),
    ]
