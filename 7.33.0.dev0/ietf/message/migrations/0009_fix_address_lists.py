# Copyright The IETF Trust 2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 14:27


from tqdm import tqdm

from django.db import migrations

import debug                            # pyflakes:ignore


def forward(apps, schema_editor):

    Message                     = apps.get_model('message', 'Message')

    for m in tqdm(Message.objects.all()):
        dirty = False
        for fieldname in ['to', 'cc', 'bcc', ]:
            f = getattr(m, fieldname)
            if f.startswith("['") or f.startswith('[]') or f.startswith("[u'"):
                l = eval(f)
                if isinstance(l, list):
                    f = ','.join(l)
                    setattr(m, fieldname, f)
                    dirty = True
        if dirty:
            m.save()

def reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('message', '0008_set_message_sent'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
