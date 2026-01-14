def find_section(soup, title):
    headers = soup.find_all(["h1", "h2", "h3", "strong"])
    for h in headers:
        if title.lower() in h.get_text(strip=True).lower():
            return h
    return None
