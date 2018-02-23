# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-08-17 00:31
from __future__ import unicode_literals

import json

from django.db import migrations
from common.models import Journal

import logging
logger = logging.getLogger('django')


EMERALD_PUBLISHING_JOURNALS = 'cos/static/EmeraldPublishing.json'


def add_emerald_published_journals(*args, **kwargs):
    with open(EMERALD_PUBLISHING_JOURNALS, 'r') as journal_file:
        emerald_published_journals = json.load(journal_file)

    for entry in emerald_published_journals:
        journal, created = Journal.objects.get_or_create(
            title=entry['title']
        )

        if created:
            journal.publisher = entry.get('publisher', '')

        journal.is_preregistered_journal = True
        journal.is_top_journal = True

        journal.save()

        logger.info('The journal {} has been successfully created, and marked for prereg and top.'.format(entry['title']))

    logger.info('{} Journals successfully imported!'.format(len(emerald_published_journals)))


def remove_emerald_published_journals(*args, **kwargs):
    with open(EMERALD_PUBLISHING_JOURNALS, 'r') as journal_file:
        emerald_published_journals = json.load(journal_file)

    for entry in emerald_published_journals:
        try:
            journal_to_remove = Journal.objects.get(
                title=entry['title'],
                publisher=entry.get('publisher', None)
            )
            journal_to_remove.delete()
            logger.info('The journal {} has been successfully deleted'.format(entry['title']))
        except Journal.DoesNotExist:
            logger.warn('The journal {} could not be found, so was not deleted'.format(entry['title']))

    logger.info('{} Journals successfully deleted!'.format(len(emerald_published_journals)))


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0055_jobs_field_to_raw_html'),
    ]

    operations = [
        migrations.RunPython(add_emerald_published_journals, remove_emerald_published_journals),
    ]
