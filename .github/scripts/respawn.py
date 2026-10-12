"""Make cells eaten by the snk snake grow back shortly after being eaten.

snk animates each cell as: @keyframes X{A%{fill:C}B%,100%{fill:var(--ce)}}
(coloured until A%, empty from B% to the end of the loop). This rewrites it to
turn empty at B% and regain colour C RESPAWN_MS later.

Usage: python respawn.py file.svg [file.svg ...]
"""
import re
import sys

RESPAWN_MS = 1500

CELL = re.compile(
    r"@keyframes (\w+)\{([\d.]+)%\{fill:(var\(--c\d\))\}([\d.]+)%,100%\{fill:var\(--ce\)\}\}"
)


def fmt(p):
    return f"{p:.3f}".rstrip("0").rstrip(".")


def patch(svg):
    duration = int(re.search(r"animation:none (\d+)ms", svg).group(1))
    gap = RESPAWN_MS / duration * 100

    def repl(m):
        name, a, color, b = m.group(1), m.group(2), m.group(3), float(m.group(4))
        back = b + gap
        if back >= 99.98:
            return m.group(0)  # loop restarts with the cell coloured anyway
        return (
            f"@keyframes {name}{{{a}%{{fill:{color}}}"
            f"{fmt(b)}%,{fmt(back)}%{{fill:var(--ce)}}"
            f"{fmt(back + 0.02)}%,100%{{fill:{color}}}}}"
        )

    return CELL.subn(repl, svg)


for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        svg, n = patch(f.read())
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{path}: {n} cells now respawn after {RESPAWN_MS} ms")
