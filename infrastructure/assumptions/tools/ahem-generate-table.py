import itertools
import unicodedata

from fontTools.ttLib import TTFont

try:
    chr(0x100)
except ValueError:
    chr = unichr

def grouper(n, iterable):
    """
    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])

ttf = TTFont("../../../fonts/Ahem.ttf")

chars = {char for table in ttf['cmap'].tables for char in table.cmap.keys()}

# exclude chars that can't be represented as HTML numeric character refs
chars = chars - (set(range(0x80, 0x9F+1)) | {0x00})

chars_sorted = sorted(chars)

per_row = 17


doctype = "<!doctype html>"
title = "<title>Ahem checker</title>"
style_open = """
<style>
* {
  padding: 0;
  margin: 0;
  border: none;
}
td {
  width: 34px;
}""".strip()
style_close = "</style>"
style_font_face = """
@font-face {
  font-family: Ahem;
  src: url("../../fonts/Ahem.ttf");
}""".strip()
style_table_font_specified = """
table {
  font: 15px/1 Ahem;
  border-collapse: separate;
  border-spacing: 1px;
  table-layout: fixed;
}""".strip()
style_table_font_unspecified = """
table {
  font-size: 15px;
  line-height: 1;
  border-collapse: separate;
  border-spacing: 1px;
  table-layout: fixed;
}""".strip()


def build_header(is_test, rel, href):
    rv = [doctype, title]

    if rel != None and href != None:
        rv.append(f'<link rel="{rel}" href="{href}">')

    rv.append(style_open)

    if is_test:
        # ahem.html
        rv.append(style_table_font_specified)

    elif rel is None and href is None:
        # ahem-notref.html
        rv.append(style_table_font_unspecified)
    else:
        rv.extend((style_font_face, style_table_font_specified))
    rv.append(style_close)

    return "\n".join(rv)


def build_table():
    rv = ["\n", "<table>\n"]

    for row in grouper(per_row, chars_sorted):
        rv.append(" " * 4 + "<tr>\n")
        for codepoint in row:
            assert codepoint <= 0xFFFF
            try:
                name = unicodedata.name(chr(codepoint))
            except ValueError:
                rv.append(" " * 8 + "<td>&#x%04X;x <!-- U+%04X -->\n" % (codepoint, codepoint))
            else:
                rv.append(" " * 8 + "<td>&#x%04X;x <!-- U+%04X: %s -->\n" % (codepoint, codepoint, name))
    rv.append("</table>\n")

    return "".join(rv)


cases = [
    # file, is_test, rel
    ("../ahem.html", True, "match"),
    ("../ahem-ref.html", False, "mismatch"),
    ("../ahem-notref.html", False, None),
]

table = build_table()

for index, case in enumerate(cases):
    next_index = index + 1
    file, is_test, rel = case
    href = cases[next_index][0][3:] if next_index < len(cases) else None
    header = build_header(is_test, rel, href)

    with open(file, "w") as file:
        file.write(f"{header}{table}")

