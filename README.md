# PDF Utils

## Setup
```sh
pip install -r requirements.txt
```

## Combine PDFs into one

```sh
python cominePdf.py combined.pdf samples/PDF1.pdf samples/PDF2.pdf
```

## Compress a PDF

Reduces file size by resampling pages as JPEG images at a lower DPI. Most effective on large scanned documents.

```sh
python compress_pdf.py output.pdf input.pdf
python compress_pdf.py output.pdf input.pdf --dpi 100
python compress_pdf.py output.pdf input.pdf --dpi 150 --quality 75
```

| Option | Default | Description |
|---|---|---|
| `--dpi` | 150 | Output resolution. Lower = smaller file. 100–150 is good for scans. |
| `--quality` | 85 | JPEG quality (1–95). Lower = smaller file, more compression artifacts. |