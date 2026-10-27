"""Flag sentences longer than 20 words in a review file.

Math spans count as one word; headers, rules and score lines are skipped.
"""
import re
import sys

for path in sys.argv[1:]:
    text = open(path).read()
    text = re.sub(r"\$[^$]*\$", "MATH", text)
    text = re.sub(r"https?://\S+", "URL", text)
    # join wrapped lines inside paragraphs/bullets
    blocks = re.split(r"\n\s*\n|\n(?=\s*[-+*]\s|\s*\d+\.\s)", text)
    n = 0
    for b in blocks:
        b = " ".join(l.strip() for l in b.splitlines())
        if not b or set(b) <= set("-=# ") or b.startswith("#"):
            continue
        b = re.sub(r"^[-+*]\s+|^\d+\.\s+", "", b)
        for s in re.split(r"(?<=[.?!])\s+(?=[A-Z0-9$`\"(])", b):
            words = [w for w in s.split() if re.search(r"\w", w)]
            if len(words) > 20:
                n += 1
                print(f"{path.split('/')[-1]}: {len(words)}w: {s[:150]}")
    print(f"{path}: {n} long sentences")
