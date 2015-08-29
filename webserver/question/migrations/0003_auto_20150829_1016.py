# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20150824_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='source_name',
            field=models.CharField(null=True, help_text='Name of source code file', max_length=30),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='source',
            field=models.TextField(null=True),
        ),
    ]
