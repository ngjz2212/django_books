# Generated by Django 3.2.7 on 2021-09-29 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_publication_book_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='book_pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
