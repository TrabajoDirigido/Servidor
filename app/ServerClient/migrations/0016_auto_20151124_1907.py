# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0015_auto_20151113_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='seccion',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lab',
            name='date',
            field=models.DateField(default='2015-11-24'),
        ),
    ]
