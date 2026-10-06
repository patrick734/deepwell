from playwright.sync_api import sync_playwright
import pathlib, base64
here = pathlib.Path(__file__).parent.resolve()
F = base64.b64encode((here / "Fraunces.woff2").read_bytes()).decode()
H = base64.b64encode((here / "HankenGrotesk.woff2").read_bytes()).decode()
BRASS, WATER, STONE, BG = "#d2a75f", "#62cdbf", "#ece6d9", "#0b1e33"


def mark(stroke=2.4):
    return f'''<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M3.5 5.5h5M23.5 5.5h5" stroke="{BRASS}" stroke-width="{stroke}" stroke-linecap="round"/><path d="M8.5 5.5v15a7.5 7.5 0 0 0 15 0v-15" fill="none" stroke="{BRASS}" stroke-width="{stroke}" stroke-linecap="round"/><path d="M12 19.5c1.3-1.3 2.7-1.3 4 0s2.7 1.3 4 0" fill="none" stroke="{WATER}" stroke-width="{stroke * 0.92}" stroke-linecap="round"/></svg>'''


base = f'''<style>@font-face{{font-family:F;src:url(data:font/woff2;base64,{F}) format("woff2");font-weight:100 900}}
@font-face{{font-family:H;src:url(data:font/woff2;base64,{H}) format("woff2");font-weight:100 900}}
html,body{{margin:0;background:{BG}}}
.d{{font-family:F;font-variation-settings:"SOFT" 100,"opsz" 144,"WONK" 1;font-weight:400}}</style>'''
bg = f"linear-gradient(180deg,#10294a 0%,{BG} 100%)"


def shafts(width, height, levels):
    cols = "".join(
        f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px">
<div style="position:relative;width:100%;height:{height}px;border:3px solid rgba(236,230,217,.3);border-top:0;border-radius:0 0 {width}px {width}px;overflow:hidden;background:rgba(4,12,22,.45)">
<div style="position:absolute;left:0;right:0;bottom:0;height:{lv}%;background:linear-gradient(180deg,{WATER},#2a7f86 70%,#1b5560)"></div></div>
<div class="d" style="font-size:{int(width * 0.36)}px;color:{STONE}">{t}</div></div>'''
        for t, lv in levels
    )
    return f'''<div style="position:relative;padding-top:26px"><div style="position:absolute;left:0;right:0;top:0;height:26px;border-top:3px solid {BRASS};background:repeating-linear-gradient(135deg,rgba(210,167,95,.25) 0 2px,transparent 2px 10px)"></div>
<div style="display:flex;gap:{int(width * 0.3)}px">{cols}</div></div>'''


LV = [("TSLA", 46), ("NVDA", 62), ("AAPL", 38), ("PLTR", 54), ("META", 70)]

logo = base + f'<div style="width:1000px;height:1000px;display:grid;place-items:center;background:{bg}"><div style="width:600px;height:600px">{mark()}</div></div>'

header = base + f'''<div style="width:1500px;height:500px;position:relative;overflow:hidden;color:{STONE};font-family:H;background:{bg}">
<div style="position:absolute;left:430px;top:132px;width:520px">
<div class="d" style="font-size:92px;line-height:1;letter-spacing:-1px">Deepwell</div>
<div style="font-size:30px;color:#c8c4b8;margin-top:22px;line-height:1.3">Earn a stock&#39;s trading fees.<br>Borrow against them.</div></div>
<div style="position:absolute;right:110px;top:70px;width:380px">{shafts(64, 250, LV)}</div></div>'''

og = base + f'''<div style="width:1200px;height:630px;position:relative;overflow:hidden;color:{STONE};font-family:H;background:{bg}">
<div style="position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:16px"><div style="width:58px;height:58px">{mark()}</div><div class="d" style="font-size:44px">Deepwell</div></div>
<div class="d" style="position:absolute;left:80px;top:200px;width:620px;font-size:80px;line-height:1.02;letter-spacing:-1.5px">Earn the trading fees of a single stock.</div>
<div style="position:absolute;left:80px;bottom:66px;font-size:24px;color:#8ea2b6">Wells and credit lines on Robinhood Chain</div>
<div style="position:absolute;right:80px;top:120px;width:340px">{shafts(56, 300, LV)}</div></div>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, w, h in [("deepwell-logo.png", logo, 1000, 1000), ("deepwell-x-header.png", header, 1500, 500), ("og.png", og, 1200, 630)]:
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(html)
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(here / name))
    b.close()
