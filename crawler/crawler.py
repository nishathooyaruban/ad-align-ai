import ipaddress
import socket
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT = (5, 15)
MAX_REDIRECTS = 5
MAX_HTML_BYTES = 3 * 1024 * 1024

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _is_public_ip(ip_text):
    """
    Return True only for globally routable IP addresses.

    This blocks loopback, private, link-local, multicast,
    reserved, unspecified, and other non-public address ranges.
    """
    try:
        ip_obj = ipaddress.ip_address(
            ip_text.split("%", 1)[0]
        )
    except ValueError:
        return False

    if (
        isinstance(ip_obj, ipaddress.IPv6Address)
        and ip_obj.ipv4_mapped is not None
    ):
        return ip_obj.ipv4_mapped.is_global

    return ip_obj.is_global


def validate_public_url(url):
    """
    Validate that a URL is an http/https URL whose hostname
    resolves only to public IP addresses.

    Raises ValueError when the URL should not be fetched.
    """
    cleaned_url = url.strip()

    if not cleaned_url:
        raise ValueError("The landing page URL is empty.")

    parsed = urlsplit(cleaned_url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(
            "Only http:// and https:// landing-page URLs are allowed."
        )

    if not parsed.hostname:
        raise ValueError("The landing page URL has no valid hostname.")

    if parsed.username or parsed.password:
        raise ValueError(
            "URLs containing embedded usernames or passwords are not allowed."
        )

    hostname = parsed.hostname.rstrip(".").lower()

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("Localhost URLs are not allowed.")

    # If the hostname itself is an IP address, validate it directly.
    try:
        direct_ip = ipaddress.ip_address(hostname)

        if not _is_public_ip(str(direct_ip)):
            raise ValueError(
                "Private, local, link-local, reserved, or internal IP "
                "addresses are not allowed."
            )

        return cleaned_url

    except ValueError as error:
        # If hostname looked like an IP and was rejected, preserve that error.
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            pass
        else:
            raise error

    try:
        address_info = socket.getaddrinfo(
            hostname,
            parsed.port or (
                443 if parsed.scheme.lower() == "https" else 80
            ),
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as error:
        raise ValueError(
            "The landing page hostname could not be resolved."
        ) from error

    resolved_ips = {
        item[4][0]
        for item in address_info
        if item and len(item) >= 5 and item[4]
    }

    if not resolved_ips:
        raise ValueError(
            "The landing page hostname did not resolve to an IP address."
        )

    for resolved_ip in resolved_ips:
        if not _is_public_ip(resolved_ip):
            raise ValueError(
                "The landing page hostname resolves to a private, local, "
                "link-local, reserved, or otherwise non-public IP address."
            )

    return cleaned_url


def _fetch_html(url):
    """
    Fetch a page while validating every redirect target.

    Redirects are handled manually so that an attacker cannot
    start with a public URL and redirect the crawler to an
    internal/private address.
    """
    current_url = validate_public_url(url)

    for redirect_count in range(MAX_REDIRECTS + 1):

        with requests.get(
            current_url,
            timeout=REQUEST_TIMEOUT,
            headers=REQUEST_HEADERS,
            allow_redirects=False,
            stream=True,
        ) as response:

            if response.is_redirect or response.is_permanent_redirect:

                if redirect_count >= MAX_REDIRECTS:
                    raise ValueError(
                        "The landing page redirected too many times."
                    )

                location = response.headers.get("Location")

                if not location:
                    raise ValueError(
                        "The landing page returned an invalid redirect."
                    )

                next_url = urljoin(
                    current_url,
                    location,
                )

                current_url = validate_public_url(
                    next_url
                )

                continue

            response.raise_for_status()

            content_type = (
                response.headers
                .get("Content-Type", "")
                .split(";", 1)[0]
                .strip()
                .lower()
            )

            allowed_content_types = {
                "text/html",
                "application/xhtml+xml",
                "",
            }

            if content_type not in allowed_content_types:
                raise ValueError(
                    "The supplied URL did not return an HTML page."
                )

            content = bytearray()

            for chunk in response.iter_content(
                chunk_size=64 * 1024
            ):
                if not chunk:
                    continue

                content.extend(chunk)

                if len(content) > MAX_HTML_BYTES:
                    raise ValueError(
                        "The landing page is too large to analyze safely."
                    )

            encoding = response.encoding or "utf-8"

            html = bytes(content).decode(
                encoding,
                errors="replace",
            )

            return current_url, html

    raise ValueError(
        "The landing page could not be fetched safely."
    )


def crawl_page(url):
    final_url, html = _fetch_html(
        url
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else ""
    )

    meta_description = ""

    meta_tag = soup.find(
        "meta",
        attrs={"name": "description"},
    )

    if meta_tag:
        meta_description = (
            meta_tag.get(
                "content",
                "",
            ).strip()
        )

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

    forms = soup.find_all(
        "form"
    )

    images = soup.find_all(
        "img"
    )

    images_with_alt = [
        img.get("alt", "").strip()
        for img in images
        if img.get("alt", "").strip()
    ]

    return {
        "url": final_url,
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
