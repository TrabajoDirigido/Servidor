# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('Names', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('lab', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('query', models.TextField()),
                ('lab', models.ForeignKey(to='ServerClient.Lab')),
            ],
        ),
    ]
