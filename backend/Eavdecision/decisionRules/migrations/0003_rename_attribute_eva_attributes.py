# Generated by Django 4.0.5 on 2022-06-14 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisionRules', '0002_decisionvalue_eva'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eva',
            old_name='attribute',
            new_name='attributes',
        ),
    ]
