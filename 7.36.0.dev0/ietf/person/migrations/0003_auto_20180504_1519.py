# Copyright The IETF Trust 2018-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-04 15:19


import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import ietf.utils.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person', '0002_auto_20180330_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEmail',
            fields=[
                ('address', models.CharField(db_index=True, max_length=64, validators=[django.core.validators.EmailValidator()])),
                ('time', models.DateTimeField(blank=True, editable=False)),
                ('primary', models.BooleanField(default=False)),
                ('origin', models.CharField(default='', editable=False, max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical email',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPerson',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(db_index=True, help_text='Preferred form of name.', max_length=255, verbose_name='Full Name (Unicode)')),
                ('ascii', models.CharField(help_text='Name as rendered in ASCII (Latin, unaccented) characters.', max_length=255, verbose_name='Full Name (ASCII)')),
                ('ascii_short', models.CharField(blank=True, help_text='Example: A. Nonymous.  Fill in this with initials and surname only if taking the initials and surname of the ASCII name above produces an incorrect initials-only form. (Blank is OK).', max_length=32, null=True, verbose_name='Abbreviated Name (ASCII)')),
                ('biography', models.TextField(blank=True, help_text='Short biography for use on leadership pages. Use plain text or reStructuredText markup.')),
                ('photo', models.TextField(blank=True, default=None, max_length=100)),
                ('photo_thumb', models.TextField(blank=True, default=None, max_length=100)),
                ('name_from_draft', models.CharField(editable=False, help_text='Name as found in a draft submission.', max_length=255, null=True, verbose_name='Full Name (from submission)')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical person',
            },
        ),
        migrations.RemoveField(
            model_name='personhistory',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personhistory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
        migrations.RemoveField(
            model_name='person',
            name='affiliation',
        ),
        migrations.AddField(
            model_name='email',
            name='origin',
            field=models.CharField(default='', editable=False, max_length=150),
        ),
        migrations.AddField(
            model_name='person',
            name='name_from_draft',
            field=models.CharField(editable=False, help_text='Name as found in a draft submission.', max_length=255, null=True, verbose_name='Full Name (from submission)'),
        ),
        migrations.DeleteModel(
            name='PersonHistory',
        ),
        migrations.AddField(
            model_name='historicalemail',
            name='person',
            field=ietf.utils.models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='person.Person'),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='consent',
            field=models.NullBooleanField(default=None, verbose_name='I hereby give my consent to the use of the personal details I have provided (photo, bio, name, email) within the IETF Datatracker'),
        ),
        migrations.AddField(
            model_name='person',
            name='consent',
            field=models.NullBooleanField(default=None, verbose_name='I hereby give my consent to the use of the personal details I have provided (photo, bio, name, email) within the IETF Datatracker'),
        ),
    ]
