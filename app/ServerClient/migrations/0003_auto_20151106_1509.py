# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0002_auto_20151009_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='query',
            name='parent',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='query',
            name='remaining_results',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='query',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='query',
            name='results',
            field=models.ManyToManyField(to='ServerClient.Result'),
        ),
    ]
