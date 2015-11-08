# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0006_query_arg1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='argument',
            name='arg_id',
        ),
        migrations.AddField(
            model_name='argument',
            name='arg1',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
