# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0003_auto_20151106_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='date',
            field=models.DateField(default='2015-11-06'),
        ),
    ]
