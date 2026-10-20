"""Write assets/chat-dark.svg and assets/chat-light.svg: an animated CortexAI chat about me.

Usage: python scripts/chat_svg.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TURNS = [
    ("Who is Abhay?",
     "An AI and cloud engineer in India. He builds multi-agent systems in Go and Python, "
     "and runs them on Google Cloud and AWS."),
    ("What has he shipped?",
     "Me, for a start: I'm CortexAI. Also HazeBusters, air quality for places with no monitor, "
     "and MemLedger, shared memory for agent teams."),
    ("Is he open to work?",
     "Yes, to software and AI engineering roles. LinkedIn is the quickest way to reach him."),
]

THEMES = {
    "dark": dict(bg="#0b0b0c", bar="#161618", text="#f2f2f2", muted="#8b8b90", user="#26262a", accent="#5CC6EE"),
    "light": dict(bg="#ffffff", bar="#f4f4f5", text="#18181b", muted="#71717a", user="#ececef", accent="#0b8fc4"),
}

W, H = 600, 352


def svg(t):
    rows, at = [], 0.3
    for q, a in TURNS:
        rows.append(f'<div class="u in" style="animation-delay:{at:.1f}s"><span>{q}</span></div>')
        dots_at, reply_at = at + 0.5, at + 1.6
        rows.append(
            '<div class="slot">'
            f'<div class="dots" style="animation-delay:{dots_at:.1f}s"><i></i><i></i><i></i></div>'
            f'<div class="b in" style="animation-delay:{reply_at:.1f}s"><div class="r">Chat · 1 credit</div>{a}</div>'
            "</div>"
        )
        at = reply_at + 1.3
    body = "".join(rows)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="A CortexAI chat: who is Abhay, what has he shipped, is he open to work">
<style>
.w{{width:{W}px;height:{H}px;background:{t['bg']};color:{t['text']};font:13px/1.45 -apple-system,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif;border-radius:12px;overflow:hidden;box-sizing:border-box}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:9px 16px;background:{t['bar']};font-size:13px}}
.top b{{font-weight:650}}.top span{{color:{t['muted']};font-size:12px}}
.c{{padding:12px 16px;display:flex;flex-direction:column;gap:8px}}
.u{{display:flex;justify-content:flex-end}}
.u span{{background:{t['user']};padding:5px 12px;border-radius:14px}}
.slot{{display:grid}}.slot>*{{grid-area:1/1}}
.b{{max-width:500px}}.r{{color:{t['accent']};font-size:11.5px;margin-bottom:1px}}
.in{{opacity:0;animation:in .45s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.dots{{opacity:0;align-self:start;padding:8px 0;animation:blink 1.1s linear forwards}}
.dots i{{display:inline-block;width:6px;height:6px;margin-right:4px;border-radius:50%;background:{t['muted']};animation:bob .9s ease-in-out infinite}}
.dots i:nth-child(2){{animation-delay:.15s}}.dots i:nth-child(3){{animation-delay:.3s}}
@keyframes blink{{0%{{opacity:0}}10%,90%{{opacity:1}}100%{{opacity:0}}}}
@keyframes bob{{0%,100%{{transform:none}}50%{{transform:translateY(-3px)}}}}
@media (prefers-reduced-motion:reduce){{.in{{animation:none;opacity:1}}.dots{{display:none}}}}
</style>
<foreignObject width="{W}" height="{H}"><div xmlns="http://www.w3.org/1999/xhtml" class="w">
<div class="top"><b>CortexAI</b><span>Who is Abhay?</span></div>
<div class="c">{body}</div>
</div></foreignObject>
</svg>
"""


for name, theme in THEMES.items():
    with open(os.path.join(ROOT, "assets", f"chat-{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg(theme))
print("wrote chat-dark.svg, chat-light.svg")
