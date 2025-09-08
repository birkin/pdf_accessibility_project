"""
Experimenting based on:
<https://github.com/docaxess/verapdf-report-generator-cli/blob/0d1495e37e8a853b0d63ae75109240c6a59572d8/app/pdf_checker/service/verapdf_checker.py#L10-L29>

Usage:
$ uv run --env-file "../.env" ./a__run_verapdf.py --pdf-path "../sample_pdfs/HH012060_1146.pdf"
"""

import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

## load constants from .env -----------------------------------------
VERAPDF_CLI_PATH: str = os.environ['VERAPDF_CLI_PATH']
OUTPUT_DIR: str = os.environ['OUTPUT_DIR']

verapdf_cli_path = Path(VERAPDF_CLI_PATH).expanduser().resolve()
output_dir = Path(OUTPUT_DIR).expanduser().resolve()
output_dir.mkdir(parents=True, exist_ok=True)


def parse_and_validate_pdf_arg() -> Path:
    """
    Parses --pdf-path arg and validates using pathlib.
    Returns a resolved Path to an existing .pdf file. Exits with a message if invalid.
    Called by main().
    """
    parser = argparse.ArgumentParser(description='Run veraPDF on a given PDF file.')
    parser.add_argument(
        '--pdf-path',
        required=True,
        help='Path to the PDF file to validate',
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        parser.error(f'File does not exist: {pdf_path}')
    if not pdf_path.is_file():
        parser.error(f'Not a file: {pdf_path}')
    if pdf_path.suffix.lower() != '.pdf':
        parser.error(f'Expected a .pdf file, got: {pdf_path.suffix}')

    return pdf_path


## manager function -------------------------------------------------


def main():
    """
    Manages script flow.
    Called by dundermain.

    Command flags:
    -f ua1 (PDF/UA-1 validation profile)
    --maxfailuresdisplayed 999999 (show all failures)
    --format json (output format)
    --success (include success messages)
    str(pdf_path) (path to pdf)
    """
    ## handle args --------------------------------------------------
    pdf_path: Path = parse_and_validate_pdf_arg()
    ## build command ------------------------------------------------
    command: list[str] = [
        str(verapdf_cli_path),
        '-f',
        'ua1',
        '--maxfailuresdisplayed',
        '999999',
        '--format',
        'json',
        '--success',
        str(pdf_path),
    ]
    ## run command --------------------------------------------------
    completed_process = subprocess.run(
        command,
        cwd='.',
        capture_output=True,
        text=True,
    )
    output = str(completed_process.stdout)
    ## save output file ---------------------------------------------
    datetime_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = output_dir / f'output_{datetime_str}.json'
    output_path.write_text(output, encoding='utf-8')
    ## print output -------------------------------------------------
    print(output)


if __name__ == '__main__':
    main()
