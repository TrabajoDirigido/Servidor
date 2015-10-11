# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientinfo',
            old_name='Names',
            new_name='names',
        ),
    ]
