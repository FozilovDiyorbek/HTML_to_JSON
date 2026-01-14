from __future__ import annotations

from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional

def _clean_text(s: str) -> str:
    return " ".join((s or "").replace("\xa0", " ").split()).strip()

def _norm(s: str) -> str:
    return _clean_text(s).lower().replace("’", "'").replace("`", "'")


def _find_section_by_title_contains(soup: BeautifulSoup, title_contains: str):
    needle = _norm(title_contains)
    for name_div in soup.select("div.step-row__name"):
        txt = _norm(name_div.get_text(" ", strip=True))
        if needle in txt:
            sec = name_div.find_parent("section")
            if sec:
                return sec
    return None


def parse_report(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    
    # 1) TOP INFO (report-info)
    
    top_info: Dict[str, str] = {}
    report_info_ul = soup.select_one("#report-info ul.report-info__content")
    if report_info_ul:
        for li in report_info_ul.select("li"):
            spans = li.select("span")
            texts = [_clean_text(s.get_text(" ", strip=True)) for s in spans]
            i = 0
            while i < len(texts) - 1:
                label = texts[i]
                value = texts[i + 1]
                if label.endswith(":"):
                    top_info[label[:-1].strip()] = value
                    i += 2
                else:
                    i += 1

    # 2) SUBYEKT (subject-info)

    subyekt: List[Dict[str, str]] = []
    keys_ul = soup.select_one("ul.subject-info__keys")
    vals_ul = soup.select_one("ul.subject-info__values")
    if keys_ul and vals_ul:
        keys = [_clean_text(li.get_text(" ", strip=True)).rstrip(":").strip() for li in keys_ul.select("li")]
        vals = [_clean_text(li.get_text(" ", strip=True)) for li in vals_ul.select("li")]
        n = min(len(keys), len(vals))
        one = {}
        for k, v in zip(keys[:n], vals[:n]):
            if k:
                one[k] = v
        if one:
            subyekt.append(one)

    # 3) SCORING (SCORING CIAC)

    scoring: Dict[str, Any] = {}
    scoring_sec = _find_section_by_title_contains(soup, "SCORING") 

    if scoring_sec:
        for li in scoring_sec.select("ul.scoring-desc li"):
            k_el = li.select_one("span")
            v_el = li.select_one("b")
            k = _clean_text(k_el.get_text(" ", strip=True)).rstrip(":").strip() if k_el else ""
            v = _clean_text(v_el.get_text(" ", strip=True)) if v_el else ""
            if k in {"SKORING BALL", "BAHOLASH SINFI", "SKORING TURI"}:
                scoring[k] = v


    # 4) UMUMLASHTIRILGAN MA'LUMOTLAR

    umumlashtirilgan: List[Dict[str, Any]] = []
    um_sec = _find_section_by_title_contains(soup, "UMUMLASHTIRILGAN")  

    if um_sec:
        for item in um_sec.select(".claims-item"):
            num_el = item.select_one(".claims-item__num")
            title_el = item.select_one(".claims-item__title")
            num = _clean_text(num_el.get_text(" ", strip=True)) if num_el else ""
            title = _clean_text(title_el.get_text(" ", strip=True)) if title_el else ""
            if num or title:
                umumlashtirilgan.append({"title": title, "count": num})


    return {
        "top_info": top_info,
        "subyekt": subyekt,
        "scoring": scoring,
        "umumlashtirilgan": umumlashtirilgan,
    }
