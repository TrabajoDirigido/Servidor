# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0011_auto_20151113_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='arguments',
            field=models.ForeignKey(default=None, to='ServerClient.Argument'),
        ),
        migrations.AlterField(
            model_name='query',
            name='results',
            field=models.ForeignKey(default=None, to='ServerClient.Result'),
        ),
    ]
