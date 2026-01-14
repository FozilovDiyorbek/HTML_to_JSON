import re
from .utils import find_section

def parse_scoring(soup):
    section = find_section(soup, "SCORING")
    if not section:
        return {}

    block = section.find_next()
    text = block.get_text(" ", strip=True)

    return {
        "skoring_ball": extract(text, "SKORING BALL"),
        "baholash_sinfi": extract(text, "BAHOLASH SINFI"),
        "skoring_turi": extract(text, "SKORING TURI")
    }

def extract(text, label):
    pattern = label + r"\s*:\s*([^\\n]+)"
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None
