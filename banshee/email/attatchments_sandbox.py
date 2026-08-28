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

import time
from email.parser import BytesParser
from pathlib import Path

import pyzipper
from psengine.config import get_config
from psengine.sandbox import SandboxMgr
from rich import print_json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from banshee.email import constants
from banshee.email.helpers import validate_eml
from banshee.sandbox.constants import SANDBOX_FRONTEND_URLS
from banshee.sandbox.samples_list import _print_sample_summary_pretty

_ZIP_PASSWORD = b"infected"

def extract_attatchments(eml_path: Path, zip_path: Path) -> list[dict[str, str]]:
    """Extract the attachment from the email file and save to a zip.

    Args:
        eml_path: Path of the EML file
        zip_path: Path to save the ZIP file to

    Returns:
        dict of extracted filenames
    """
    attatchments = []

    with Path(eml_path).open("rb") as f:
        parsed_email = BytesParser().parse(f)

    with pyzipper.AESZipFile(
        zip_path,
        mode="w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zip_file:
       zip_file.setpassword(_ZIP_PASSWORD)

       for part in parsed_email.walk():
           content_disposition = part.get_content_disposition()

           if content_disposition == "attachment" and part.get_filename() not in attatchments:
                attatchments.append(part.get_filename())
                zip_file.writestr(
                    part.get_filename(),
                    part.get_payload(decode=True)
                )

    return attatchments

def _empty_error(msg, pretty):
    if pretty:
        print(msg)
    else:
        print([])

def sandbox_attatchments(file_path, zip_path, pretty):
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
        console=Console(stderr=True)
    ) as progress:
        validate_eml(file_path)

        task_id = progress.add_task(description="Extracting files")
        output_path = Path(zip_path) / "extracted_files.zip"

        attatchments = extract_attatchments(file_path, output_path)

        if not attatchments:
            _empty_error(
                f"No files were extracted from {file_path}",
                pretty
            )
            return

        progress.update(
            task_id,
            description=f"Submitting ZIP file with {len(attatchments)} files to sandbox"
        )
        sandbox_mgr = SandboxMgr()
        submission = sandbox_mgr.submit_sample(
            kind="file",
            file_path=output_path,
            password=str(_ZIP_PASSWORD),
            user_tags="Banshee EML Extraction"
        )

        progress.update(task_id, description="Waiting for Sandbox Analysis...")
        deadline = time.monotonic() + constants.SANDBOX_TIMEOUT
        while time.monotonic() < deadline:
            report = sandbox_mgr.fetch_sample(submission.id_)
            if report.status in constants.SANDBOX_COMPLETED_STATUS:
                break
            time.sleep(constants.SANDBOX_POLL_RATE)
        else:
            _empty_error(
                f"Failed to get report for submission {submission.id_}. Timed out.",
                pretty
            )
            return

        summary = sandbox_mgr.fetch_sample_summary(submission.id_)

    if pretty:
        sandbox_region = get_config().sandbox_choice
        gui_url = SANDBOX_FRONTEND_URLS.get(sandbox_region, SANDBOX_FRONTEND_URLS['eu'])
        _print_sample_summary_pretty(summary, gui_url)
    else:
        print_json(summary.model_dump_json())
