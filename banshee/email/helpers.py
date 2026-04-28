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

import hashlib
import json
import mimetypes
import sys
from email.parser import BytesParser
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Annotated

from psengine.common_models import RFBaseModel
from pydantic import BeforeValidator, Field, HttpUrl, IPvAnyAddress


def arrange_data(data) -> list[str]:
    data = json.loads(data)
    return sorted(data.values())


def get_mime_type(path: str) -> str:
    if sys.version_info.major == 3 and sys.version_info.minor < 13:
        mime_type = mimetypes.guess_type(path)
    else:
        mime_type = mimetypes.guess_file_type(path)
    return mime_type


def validate_eml(eml_path: str) -> None:
    """Validates an EML file
    Args:
        eml_path: The path to the EML file.
    """
    eml_path = Path(eml_path)

    if not eml_path.exists():
        raise RuntimeError(f'{eml_path} was not found')
    mime_type = get_mime_type(eml_path)
    if not mime_type[0] == 'message/rfc822':
        raise RuntimeError(f'{eml_path} is file type {mime_type[0]}. Expected "message/rfc822"')
    if eml_path.stat().st_size <= 0:
        raise RuntimeError(f'{eml_path} size is 0 bytes')


def parse_eml(eml_path: Path) -> tuple[tuple, dict, dict[str, str]]:
    """Extract the entities from the email file.

    Args:
        eml_path: Path to the EML file

    Returns:
        list of (key, value) pairs for the header items
        dict of the emails body/contents. "text/plain" and/or "text/html"
        list of dictionaries of the attachments. In the form {"name":..., "hash":...}
    """
    with Path.open(eml_path, 'rb') as f:
        parsed_email = BytesParser().parse(f)

        headers = [[key, value] for key, value in parsed_email.items()]

        body = {}
        attachments = []
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            content_disposition = part.get_content_disposition()

            if content_type == 'text/plain' or content_type == 'text/html':
                body[content_type] = (
                    part.get_payload(decode=True)
                    .decode(part.get_content_charset(), errors='replace')
                    .replace('\n', '')
                )

            elif content_disposition == 'attachment':
                attachment_name = part.get_filename()
                attachment_content = part.get_payload(decode=True)
                sha265 = hashlib.sha256(attachment_content).hexdigest()
                attachments.append({'name': attachment_name, 'hash': sha265})

    return (headers, body, attachments)


class TARisklist(RFBaseModel):
    """Custom TA Risklist validator."""

    ioc: str = Field(validation_alias='Name')
    ta_names: Annotated[list[str], BeforeValidator(arrange_data)] = Field(
        validation_alias='ThreatActorNames'
    )


class URL(RFBaseModel):
    """Model to validate URL."""

    url: HttpUrl


class IP(RFBaseModel):
    """Model to validate IP."""

    ip: IPvAnyAddress


class HrefExtractor(HTMLParser):
    """Class to extract HTML links."""

    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.text_chunks = []

    def handle_starttag(self, tag, attrs):
        """Extract value from `a` and `href` tags."""
        if tag.lower() != 'a':
            return

        for name, value in attrs:
            if name.lower() == 'href' and value:
                self.hrefs.append(unescape(value))

    def handle_data(self, data):
        """Avoid duplication helper."""
        if data:
            self.text_chunks.append(data)
