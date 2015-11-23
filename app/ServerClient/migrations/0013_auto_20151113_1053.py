# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0012_auto_20151113_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='arguments',
            field=models.ForeignKey(to='ServerClient.Argument', null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='results',
            field=models.ForeignKey(to='ServerClient.Result', null=True),
        ),
    ]
