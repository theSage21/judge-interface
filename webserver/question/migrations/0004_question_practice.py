# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20150829_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='practice',
            field=models.BooleanField(default=False),
        ),
    ]
