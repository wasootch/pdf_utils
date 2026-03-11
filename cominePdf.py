import sys
from pathlib import Path

from PyPDF2 import PdfMerger

def merge_pdfs(input_files, output_file):
    """
    Merge multiple PDF files into a single PDF.

    :param input_files: list of paths to input PDF files
    :param output_file: path to the resulting merged PDF file
    """
    merger = PdfMerger()
    try:
        for pdf in input_files:
            merger.append(str(pdf))

        merger.write(str(output_file))
    finally:
        merger.close()


def main(argv=None):
    """
    Usage:
        python cominedPdf.py output.pdf input1.pdf input2.pdf ...
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) < 3:
        print("Usage: python cominedPdf.py output.pdf input1.pdf input2.pdf ...")
        sys.exit(1)

    output = Path(argv[0])
    inputs = [Path(p) for p in argv[1:]]

    missing = [p for p in inputs if not p.is_file()]
    if missing:
        print("These input files do not exist:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    # Ensure the output directory exists before writing
    out_dir = Path(output).parent
    if out_dir and not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    merge_pdfs(inputs, output)
    print(f"Merged {len(inputs)} PDF(s) into: {output}")


if __name__ == "__main__":
    main()

