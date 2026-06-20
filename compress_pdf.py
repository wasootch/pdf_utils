import sys
from pathlib import Path

import fitz  # PyMuPDF

_RED = "\033[91m"
_RESET = "\033[0m"


def _colorize(text, color):
    if sys.stdout.isatty():
        return f"{color}{text}{_RESET}"
    return text


def compress_pdf(input_file, output_file, dpi=150, jpeg_quality=85):
    src = fitz.open(str(input_file))
    out = fitz.open()

    for page in src:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_page = out.new_page(width=page.rect.width, height=page.rect.height)
        img_page.insert_image(img_page.rect, stream=pix.tobytes("jpeg", jpg_quality=jpeg_quality))

    out.save(str(output_file), garbage=4, deflate=True)
    src.close()
    out.close()


def main(argv=None):
    """
    Usage:
        python compress_pdf.py output.pdf input.pdf [--dpi 150] [--quality 85]
    """
    if argv is None:
        argv = sys.argv[1:]

    dpi = 150
    jpeg_quality = 85
    args = []
    i = 0
    while i < len(argv):
        if argv[i] in ("--dpi", "-dpi") and i + 1 < len(argv):
            dpi = int(argv[i + 1])
            i += 2
        elif argv[i] in ("--quality", "-quality") and i + 1 < len(argv):
            jpeg_quality = int(argv[i + 1])
            i += 2
        else:
            args.append(argv[i])
            i += 1

    if len(args) < 2:
        print("Usage: python compress_pdf.py output.pdf input.pdf [--dpi 150] [--quality 85]")
        sys.exit(1)

    output = Path(args[0])
    input_file = Path(args[1])

    if not input_file.is_file():
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    out_dir = output.parent
    if out_dir and not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    before_kb = input_file.stat().st_size / 1024
    compress_pdf(input_file, output, dpi=dpi, jpeg_quality=jpeg_quality)
    after_kb = output.stat().st_size / 1024

    pct = 100 * (1 - after_kb / before_kb)
    size_line = f"  Before: {before_kb:,.0f} KB  After: {after_kb:,.0f} KB  ({pct:.0f}% reduction)"
    if after_kb > before_kb:
        size_line = _colorize(size_line, _RED)

    print(f"Compressed: {input_file} -> {output}")
    print(size_line)


if __name__ == "__main__":
    main()
