# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0010_auto_20151113_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='arguments',
        ),
        migrations.AddField(
            model_name='query',
            name='arguments',
            field=models.ForeignKey(to='ServerClient.Argument', default=1),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='query',
            name='results',
        ),
        migrations.AddField(
            model_name='query',
            name='results',
            field=models.ForeignKey(to='ServerClient.Result', default=1),
            preserve_default=False,
        ),
    ]
