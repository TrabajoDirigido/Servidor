# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0013_auto_20151113_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='arguments',
        ),
        migrations.RemoveField(
            model_name='query',
            name='results',
        ),
        migrations.AddField(
            model_name='argument',
            name='query',
            field=models.OneToOneField(default=1, to='ServerClient.Query'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='query',
            field=models.OneToOneField(default=1, to='ServerClient.Query'),
            preserve_default=False,
        ),
    ]
