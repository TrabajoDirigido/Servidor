# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0005_auto_20151107_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='arg1',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
