import requests
from bs4 import BeautifulSoup


def crawl_page(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})

    if meta_tag:
        meta_description = meta_tag.get("content", "").strip()

    headings = {
        "h1": [
            h.get_text(" ", strip=True)
            for h in soup.find_all("h1")
        ],
        "h2": [
            h.get_text(" ", strip=True)
            for h in soup.find_all("h2")
        ],
        "h3": [
            h.get_text(" ", strip=True)
            for h in soup.find_all("h3")
        ],
    }

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.find_all("p")
        if p.get_text(strip=True)
    ]

    links = [
        a.get_text(" ", strip=True)
        for a in soup.find_all("a")
        if a.get_text(strip=True)
    ]

    buttons = [
        button.get_text(" ", strip=True)
        for button in soup.find_all("button")
        if button.get_text(strip=True)
    ]

    forms = soup.find_all("form")

    images = soup.find_all("img")

    images_with_alt = [
        img.get("alt", "").strip()
        for img in images
        if img.get("alt", "").strip()
    ]

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "buttons": buttons,
        "form_count": len(forms),
        "image_count": len(images),
        "images_with_alt": images_with_alt,
    }