# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0014_auto_20151113_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='query',
            field=models.ForeignKey(to='ServerClient.Query'),
        ),
        migrations.AlterField(
            model_name='result',
            name='query',
            field=models.ForeignKey(to='ServerClient.Query'),
        ),
    ]
