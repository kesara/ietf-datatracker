# Generated by Django 2.2.17 on 2020-12-10 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liaisons', '0008_purge_liaisonstatementgroupcontacts_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LiaisonStatementGroupContacts',
        ),
    ]
