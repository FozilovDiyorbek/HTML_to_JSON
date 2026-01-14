def parse_top_info(soup):
    data = {}
    
    container = soup.find("ul", class_="report-info__content")
    if not container:
        return data

    for li in container.find_all("li"):
        spans = li.find_all("span")
        i = 0
        while i < len(spans) - 1:
            key = spans[i].get_text(strip=True).replace(":", "")
            value = spans[i+1].get_text(strip=True)
            data[key] = value
            i += 2

    return data
