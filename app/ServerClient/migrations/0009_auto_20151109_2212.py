# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0008_auto_20151108_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='name',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lab',
            name='date',
            field=models.DateField(default='2015-11-09'),
        ),
    ]
