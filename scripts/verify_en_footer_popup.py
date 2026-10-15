#!/usr/bin/env python3
"""Guard the EN homepage's existing animated floating footer behavior."""
from html.parser import HTMLParser
from pathlib import Path
import re

home_template = Path("layouts/index.html").read_text(encoding="utf-8")
base_css = Path("assets/css/_override.scss").read_text(encoding="utf-8")
footer_template = Path("layouts/partials/footer.html").read_text(encoding="utf-8")

# The EN-specific visual styling must not override the shared footer animation.
assert not re.search(
    r"\.custom-footer--en-home\s*\{[^}]*\bposition\s*:\s*static",
    home_template,
    re.I,
), "EN homepage forces the footer static and disables popup"
assert not re.search(
    r"\.footer-reserve\s*\{[^}]*\bheight\s*:\s*0\s*!important",
    home_template,
    re.I,
), "EN homepage removes the reserved footer space"

floating = re.search(r"body\.footer-floating\s+\.custom-footer\s*\{([^}]+)\}", base_css)
popup = re.search(
    r"body\.footer-floating\.footer-popup-visible\s+\.custom-footer\s*\{([^}]+)\}",
    base_css,
)
assert floating and re.search(r"position\s*:\s*fixed", floating.group(1)), (
    "Shared floating footer positioning absent"
)
assert popup and re.search(r"bottom\s*:\s*0\s*;", popup.group(1)), (
    "Shared footer reveal transition absent"
)
assert "function showPopupNow(" in footer_template
assert "function hidePopupWhileReading(" in footer_template
assert 'classList.add("footer-popup-visible")' in footer_template
assert 'classList.remove("footer-popup-visible")' in footer_template

class Footers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.classes = []
    def handle_starttag(self, tag, attrs):
        if tag == "footer":
            self.classes.append(dict(attrs).get("class", ""))

page = Footers()
page.feed(Path("public/index.html").read_text(encoding="utf-8"))
assert any("custom-footer--en-home" in x.split() for x in page.classes), (
    "Expected EN homepage footer is missing from rendered HTML"
)
print("PASS: EN homepage preserves original footer popup animation and reserve")
