"""Interaction tests for a reading deck (Playwright Firefox).

usage: python3 -I tools/interact.py URL
Finds the build slides from BUILDS at run time, so it works on any deck made from the template.
Checks: step counts forward and back, backward entry, forward entry, #k jumps, T/N/Q/resize
mid-build, B and Q across reload, the question list on #allq, reduced motion, console errors.
"""
import sys

from playwright.sync_api import sync_playwright

url = sys.argv[1].split('#')[0]
fails = []


def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


def ready(pg):
    pg.wait_for_function("document.documentElement.classList.contains('math-ready')", timeout=15000)


with sync_playwright() as p:
    br = p.firefox.launch()
    ctx = br.new_context(viewport={'width': 1280, 'height': 800})
    ctx.add_init_script("try{if(!sessionStorage.getItem('init')){localStorage.clear();sessionStorage.setItem('init','1')}}catch(e){}")
    pg = ctx.new_page()
    errs, cons = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: cons.append(m.text) if m.type == 'error' else None)
    pg.goto(url, wait_until='networkidle')
    ready(pg)
    n = pg.evaluate('slides.length')
    # build slides: [slide index, figure id, steps], only figures with 2 or more steps
    bs = pg.evaluate('''(function(){var r=[]; for (var i=0;i<slides.length;i++){var sv=slides[i].querySelector('.fig > svg');
        if (sv && BUILDS[sv.id] >= 2) r.push([i, sv.id, BUILDS[sv.id]]);} return r;})()''')
    check(len(bs) > 0, f'deck has build slides: {bs}')
    exp = pg.evaluate('''(function(){var t=0; for (var i=0;i<slides.length;i++){var sv=slides[i].querySelector('.fig > svg');
        t += (sv && BUILDS[sv.id]) ? BUILDS[sv.id] : 1;} return t - 1;})()''')
    cnt = 0
    for _ in range(exp + 20):
        before = pg.evaluate('[cur, document.getElementById("count").textContent]')
        pg.keyboard.press('ArrowRight')
        pg.wait_for_timeout(15)
        if pg.evaluate('[cur, document.getElementById("count").textContent]') == before:
            break
        cnt += 1
    check(cnt == exp, f'forward advances {cnt} == expected {exp} ({n} slides)')
    check(pg.evaluate('cur') == n - 1, 'forward walk ends on the last slide')
    back = 0
    for _ in range(exp + 20):
        before = pg.evaluate('[cur, document.getElementById("count").textContent]')
        pg.keyboard.press('ArrowLeft')
        pg.wait_for_timeout(15)
        if pg.evaluate('[cur, document.getElementById("count").textContent]') == before:
            break
        back += 1
    check(pg.evaluate('cur') == 0 and back == exp, f'backward walk returns to slide 1 ({back} steps)')
    if bs:
        a, aid, an = bs[0]
        z, zid, zn = bs[-1]
        if a + 1 < n:
            pg.evaluate(f'show({a + 1}, "jump", "fwd")')
            pg.keyboard.press('ArrowLeft')
            check(pg.evaluate('cur') == a and pg.evaluate(f'effStep("{aid}")') == an, f'backward entry to slide {a + 1} lands on its final step')
        pg.evaluate(f'show({a}, "jump", "fwd")')
        s1 = pg.evaluate(f'effStep("{aid}")')
        pg.keyboard.press('ArrowRight')
        check(s1 == 1 and pg.evaluate('cur') == a and pg.evaluate(f'effStep("{aid}")') == 2, f'forward entry to slide {a + 1} starts at step 1, then step 2')
        pg.goto(url + f'#{z + 1}', wait_until='networkidle')
        ready(pg)
        check(pg.evaluate('cur') == z and pg.evaluate(f'effStep("{zid}")') == zn, f'#{z + 1} jump shows slide {z + 1} in its final state')
        pg.evaluate(f'show({a}, "jump", "fwd")')
        pg.keyboard.press('ArrowRight')
        s0 = pg.evaluate(f'effStep("{aid}")')
        pg.keyboard.press('t'); pg.wait_for_timeout(100)
        check(pg.evaluate('document.documentElement.getAttribute("data-theme")') == 'dark' and pg.evaluate(f'effStep("{aid}")') == s0, f'T switches theme and keeps step {s0}')
        pg.keyboard.press('n'); pg.wait_for_timeout(100)
        check(pg.evaluate('document.body.classList.contains("show-notes")') and pg.evaluate(f'effStep("{aid}")') == s0, 'N shows notes and keeps the step')
        pg.keyboard.press('n')
        pg.keyboard.press('q'); pg.wait_for_timeout(100)
        check(pg.evaluate('document.body.classList.contains("hide-qs")') and pg.evaluate(f'effStep("{aid}")') == s0, 'Q hides the questions and keeps the step')
        pg.set_viewport_size({'width': 1100, 'height': 760}); pg.wait_for_timeout(400)
        check(pg.evaluate(f'effStep("{aid}")') == s0, 'resize keeps the step')
        if s0 < an:
            hidden = pg.evaluate(f'''(function(){{var h=0; document.querySelectorAll('#{aid} g[data-b]').forEach(function(x){{ if (x.style.visibility==='hidden') h++; }}); return h;}})()''')
            check(hidden > 0, f'groups above the current step stay hidden after resize ({hidden})')
        pg.keyboard.press('b'); pg.wait_for_timeout(100)
        pg.reload(wait_until='networkidle')
        ready(pg)
        check(pg.evaluate('buildsOn') is False, 'B (builds off) persists across reload')
        check(pg.evaluate('document.documentElement.getAttribute("data-theme")') == 'dark', 'theme persists across reload')
        check(pg.evaluate('document.body.classList.contains("hide-qs")'), 'Q (questions hidden) persists across reload')
        pg.keyboard.press('b'); pg.keyboard.press('q')
    chips = pg.evaluate("document.querySelectorAll('.qs .q').length")
    listed = pg.evaluate("document.querySelectorAll('#allq li').length")
    has_allq = pg.evaluate("!!document.getElementById('allq')")
    check(not has_allq or chips == listed, f'#allq lists every question chip ({listed} of {chips})')
    check(not errs, f'no page errors {errs}')
    check(not cons, f'no console errors {cons}')
    ctx.close()
    if bs:
        ctx2 = br.new_context(viewport={'width': 1280, 'height': 800}, reduced_motion='reduce')
        pg2 = ctx2.new_page()
        pg2.goto(url + f'#{a + 1}', wait_until='networkidle')
        ready(pg2)
        pg2.evaluate(f'show({a}, "jump", "fwd")')
        s1 = pg2.evaluate(f'effStep("{aid}")')
        pg2.keyboard.press('ArrowRight')
        check(pg2.evaluate('cur') == a and s1 == 1 and pg2.evaluate(f'effStep("{aid}")') == 2, 'reduced motion keeps the steps (1 -> 2)')
        ctx2.close()
    br.close()
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
