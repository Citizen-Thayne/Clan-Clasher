# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClanClasher', '0005_auto_20150412_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chief',
            name='level',
            field=models.IntegerField(choices=[(3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
            preserve_default=True,
        ),
    ]
