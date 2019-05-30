# Generated by Django 2.1.5 on 2019-05-16 05:36

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageContents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDelete', models.BooleanField(default=False)),
                ('mess_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('mess_username', models.CharField(max_length=20)),
                ('mess_contents', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'message_contents',
                'abstract': False,
            },
            managers=[
                ('my_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
