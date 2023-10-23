# Generated by Django 4.1.2 on 2023-06-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomAPODText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('media_type', models.CharField(max_length=25, null=True)),
                ('link', models.CharField(max_length=255, null=True, unique=True)),
                ('message', models.CharField(max_length=2000)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]