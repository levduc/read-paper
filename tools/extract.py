"""Extract a paper PDF: Markdown text plus one PNG per page.

usage: python3 -I tools/extract.py PAPER.pdf OUTDIR [--dpi 110] [--pages-only]
Writes OUTDIR/paper.md (pymupdf4llm, OCR off, page separators on) and OUTDIR/pages/pNN.png.
--pages-only writes only the PNGs (use it after the MCP made paper.md).

Use this when the PyMuPDF4LLM MCP fails (for example "Tesseract language initialisation
failed" when tessdata has no eng.traineddata). If pymupdf4llm is not installed, the script
re-runs itself under `uvx --from pymupdf4llm-mcp@latest --with pymupdf4llm`.
pymupdf4llm drops display equations: read them from the page PNGs.
"""
import inspect
import os
import shutil
import subprocess
import sys


def markdown(pdf, out):
    import pymupdf4llm
    kw = dict(page_separators=True)
    ps = inspect.signature(pymupdf4llm.to_markdown).parameters
    if 'use_ocr' in ps or any(v.kind == v.VAR_KEYWORD for v in ps.values()):
        kw['use_ocr'] = False  # OCR needs tessdata, and born-digital papers do not need it
    md = pymupdf4llm.to_markdown(pdf, **kw)
    with open(os.path.join(out, 'paper.md'), 'w') as f:
        f.write(md)
    print(f'paper.md: {len(md)} chars (pymupdf4llm {pymupdf4llm.__version__})')


def pages(pdf, out, dpi):
    import pymupdf
    d = os.path.join(out, 'pages')
    os.makedirs(d, exist_ok=True)
    doc = pymupdf.open(pdf)
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=dpi).save(os.path.join(d, f'p{i + 1:02d}.png'))
    print(f'pages/: {doc.page_count} PNGs at {dpi} dpi')


def main():
    args = sys.argv[1:]
    md_only = '--md-only' in args
    dpi = 110
    if '--dpi' in args:
        dpi = int(args[args.index('--dpi') + 1])
    pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--dpi')]
    if len(pos) != 2:
        sys.exit(__doc__)
    pdf, out = os.path.abspath(pos[0]), os.path.abspath(pos[1])
    os.makedirs(out, exist_ok=True)
    if '--pages-only' in args:
        pages(pdf, out, dpi)
        return
    try:
        markdown(pdf, out)
    except ImportError:
        if md_only or not shutil.which('uvx'):
            sys.exit('pymupdf4llm is missing: pip install pymupdf4llm, or install uv (uvx).')
        print('pymupdf4llm not installed here; running under uvx ...')
        try:
            import pymupdf  # noqa: F401  -- render the pages here if this Python has PyMuPDF
            extra = ['--md-only']
        except ImportError:
            extra = ['--dpi', str(dpi)]
        subprocess.run(['uvx', '--from', 'pymupdf4llm-mcp@latest', '--with', 'pymupdf4llm',
                        'python', '-I', os.path.abspath(__file__), pdf, out] + extra, check=True)
        if extra[0] != '--md-only':
            return
    if not md_only:
        pages(pdf, out, dpi)
        print('Reminder: display equations are missing from paper.md. Read them from pages/pNN.png.')


if __name__ == '__main__':
    main()
