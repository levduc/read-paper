"""Screenshot every slide and build step of a reading deck with Playwright Firefox.

usage: python3 -I shoot.py URL OUTDIR [--slides 1,2,5] [--narrow] [--themes light,dark]
Writes OUTDIR/<theme>-<w>/sNN-bK.png, a report of console errors and overflows, and contact sheets.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw


def main():
    url, out = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    only = None
    themes = ['light', 'dark']
    narrow = '--narrow' in args
    if '--slides' in args:
        only = {int(x) for x in args[args.index('--slides') + 1].split(',')}
    if '--themes' in args:
        themes = args[args.index('--themes') + 1].split(',')
    sizes = [(390, 844)] if narrow else [(1280, 800)]
    report = {'errors': [], 'overflow': []}
    with sync_playwright() as p:
        br = p.firefox.launch()
        for theme in themes:
            for (w, h) in sizes:
                d = os.path.join(out, f'{theme}-{w}')
                os.makedirs(d, exist_ok=True)
                ctx = br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce')
                ctx.add_init_script(f"try{{localStorage.setItem('rp-theme','{theme}');localStorage.setItem('rp-builds','on')}}catch(e){{}}")
                pg = ctx.new_page()
                pg.on('console', lambda m: report['errors'].append(f'{theme}-{w} console {m.type}: {m.text}') if m.type in ('error', 'warning') and 'downloadable font' not in m.text and 'mathvariant' not in m.text else None)
                pg.on('pageerror', lambda e: report['errors'].append(f'{theme}-{w} pageerror: {e}'))
                pg.goto(url, wait_until='networkidle')
                try:
                    pg.wait_for_function("document.documentElement.classList.contains('math-ready')", timeout=15000)
                except Exception as e:  # noqa: BLE001
                    report['errors'].append(f'{theme}-{w} math-ready timeout: {e}')
                pg.wait_for_timeout(600)
                n = pg.evaluate('slides.length')
                if narrow:
                    total = pg.evaluate('document.documentElement.scrollHeight')
                    hs = pg.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth')
                    if hs:
                        report['overflow'].append(f'{theme}-{w}: horizontal scroll')
                    for i in range(n):
                        if only and (i + 1) not in only:
                            continue
                        el = pg.locator('.slide').nth(i)
                        el.screenshot(path=os.path.join(d, f's{i + 1:02d}.png'))
                    report['narrow_height'] = total
                    continue
                for i in range(n):
                    if only and (i + 1) not in only:
                        continue
                    pg.evaluate(f'show({i}, "jump", "fwd")')
                    bid = pg.evaluate(f'buildFig({i})')
                    steps = pg.evaluate(f'BUILDS["{bid}"]') if bid else 1
                    for s in range(1, steps + 1):
                        if bid and s > 1:
                            pg.evaluate(f'setStep("{bid}", {s}, false)')
                        pg.wait_for_timeout(120)
                        pg.screenshot(path=os.path.join(d, f's{i + 1:02d}-b{s}.png'))
                    ov = pg.evaluate(f'''(function(){{var sl=slides[{i}], r=sl.getBoundingClientRect(), bad=[];
                        sl.querySelectorAll('*').forEach(function(e){{ if (e.closest('.notes') || e.closest('.katex-mathml')) return; var b=e.getBoundingClientRect();
                          if (b.width && b.height && (b.bottom > r.bottom + 1 || b.right > window.innerWidth + 1)) bad.push(e.tagName + '.' + (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className) + ' ' + Math.round(b.bottom) + '>' + Math.round(r.bottom)); }});
                        return bad.slice(0, 5);}})()''')
                    if ov:
                        report['overflow'].append(f'{theme}-{w} slide {i + 1}: {ov}')
                ctx.close()
        br.close()
    with open(os.path.join(out, 'report.json'), 'w') as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report, indent=1))
    # contact sheets
    for sub in sorted(os.listdir(out)):
        d = os.path.join(out, sub)
        if not os.path.isdir(d):
            continue
        files = sorted(x for x in os.listdir(d) if x.endswith('.png'))
        if not files:
            continue
        thumbs = []
        for fn in files:
            im = Image.open(os.path.join(d, fn)).convert('RGB')
            im.thumbnail((640, 640))
            thumbs.append((fn, im))
        cols = 3
        tw_, th_ = max(t.width for _, t in thumbs), max(t.height for _, t in thumbs) + 18
        for start in range(0, len(thumbs), 12):
            chunk = thumbs[start:start + 12]
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * tw_, rows * th_), 'white')
            dr = ImageDraw.Draw(sheet)
            for k, (fn, t) in enumerate(chunk):
                x, y = (k % cols) * tw_, (k // cols) * th_
                sheet.paste(t, (x, y + 18))
                dr.text((x + 4, y + 2), fn, fill='black')
            sheet.save(os.path.join(out, f'sheet-{sub}-{start // 12 + 1}.png'))


if __name__ == '__main__':
    main()
