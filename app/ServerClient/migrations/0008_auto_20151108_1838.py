# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0007_auto_20151107_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='origin',
            field=models.CharField(default='localhost', max_length=200),
        ),
        migrations.AlterField(
            model_name='lab',
            name='date',
            field=models.DateField(default='2015-11-08'),
        ),
    ]
