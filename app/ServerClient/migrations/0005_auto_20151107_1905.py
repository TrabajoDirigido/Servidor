# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ServerClient', '0004_lab_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('value', models.TextField()),
                ('type', models.CharField(max_length=100)),
                ('arg_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='query',
            name='remaining_args',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lab',
            name='date',
            field=models.DateField(default='2015-11-07'),
        ),
        migrations.AddField(
            model_name='query',
            name='arguments',
            field=models.ManyToManyField(to='ServerClient.Argument'),
        ),
    ]
