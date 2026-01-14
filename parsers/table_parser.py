from .utils import find_section

def parse_table_after_header(soup, header_text):
    header = find_section(soup, header_text)
    if not header:
        return []

    table = header.find_next("table")
    if not table:
        return []

    heads = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []

    for tr in table.find_all("tr")[1:]:
        vals = [td.get_text(strip=True) for td in tr.find_all("td")]
        rows.append(dict(zip(heads, vals)))

    return rows
