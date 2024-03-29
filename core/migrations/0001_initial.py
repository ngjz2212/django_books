# Generated by Django 3.0.7 on 2021-01-16 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.TextField()),
                ('publisher_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.TextField()),
                ('title', models.TextField()),
                ('author_id', models.TextField()),
                ('summary', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
    ]
