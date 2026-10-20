#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

import csv
import sys

from psengine.analyst_notes import AnalystNote
from psengine.common_models import RFBaseModel
from pydantic import HttpUrl

CSV_FIELDNAMES = ['ID', 'Title', 'Note Text', 'Note Entities', 'Published', 'Topics','Source Name', 'Portal Url']


def sanitize_csv_field(text):
    """Sanitise a CSV field for writing to the console. Remove line breaks and commas."""
    if text is None:
        return ''

    return str(text).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace(',', ' ').strip()


def _parse_note_entities(note_entities: list):
    """Return the note entities as a formatted string"""
    if note_entities is None:
        return ''
    else:
        entities = []
        for entity in note_entities:
            entities.append(f"{entity.id}:{entity.name}")
        return ' '.join(entities)


def _parse_topics(topics: list):
    """Parse topics from an Analyst Note and return an array."""
    if topics is None:
        return []
    else:
        topics = []
        for topic in topics:
            topics.append(topic.name)
        return ' '.join(topics)


def format_as_csv(notes: list[AnalystNote]):
    """Take a list of analyst notes and format them for printing in a CSV format to the conosle."""
    writer = csv.DictWriter(sys.stdout, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()
    for note in notes:
        writer.writerow(
            {
                'ID': note.id_,
                'Title': note.attributes.title,
                'Note Text': sanitize_csv_field(note.attributes.text),
                'Note Entities': _parse_note_entities(note.attributes.note_entities),
                'Published': note.attributes.published,
                'Topics': _parse_topics(note.attributes.topic),
                'Source Name': note.source.name,
                'Portal Url': note.portal_url,
            }
        )


class URL(RFBaseModel):
    """Model to validate URL."""

    url: HttpUrl
