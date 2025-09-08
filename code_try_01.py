"""
Experimenting based on:
<https://github.com/docaxess/verapdf-report-generator-cli/blob/0d1495e37e8a853b0d63ae75109240c6a59572d8/app/pdf_checker/service/verapdf_checker.py#L10-L29>
"""

import argparse
import os
import subprocess
from pathlib import Path

## load constants ---------------------------------------------------
try:
    VERAPDF_CLI_PATH: str = os.environ['VERAPDF_CLI_PATH']
except KeyError:
    raise ValueError('VERAPDF_CLI_PATH environment variable must be set')

try:
    OUTPUT_DIR: str = os.environ['OUTPUT_DIR']
except KeyError:
    raise ValueError('OUTPUT_DIR environment variable must be set')

verapdf_cli_path = Path(VERAPDF_CLI_PATH).expanduser().resolve()
output_dir = Path(OUTPUT_DIR).expanduser().resolve()
output_dir.mkdir(parents=True, exist_ok=True)


def parse_and_validate_pdf_path() -> Path:
    """Parse CLI args and validate --pdf-path using pathlib.

    Returns a resolved Path to an existing .pdf file. Exits with a message if invalid.
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


def main():
    pdf_path = parse_and_validate_pdf_path()
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
    completed_process = subprocess.run(
        command,
        cwd='.',
        capture_output=True,
        text=True,
    )
    output = str(completed_process.stdout)
    output_path = output_dir / pdf_path.name
    output_path.write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
