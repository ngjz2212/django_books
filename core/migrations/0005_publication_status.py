# Generated by Django 3.0.7 on 2021-01-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], default='d', max_length=1),
        ),
    ]