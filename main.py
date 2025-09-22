# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
from telegram_bot import send_telegram_message  # unchanged

user_name = "xorioo10"

API_URL = f"https://media.mollygram.com/?url={user_name}&method=allstories"
TINYURL_API = "http://tinyurl.com/api-create.php?url="
LINKS_DB = "links.json"
POLL_SECONDS = 30
REQUEST_TIMEOUT = 20


def get_id(url: str) -> str | None:
    """
    Reproduces your previous ID extraction from anon-viewer URLs.
    Prefers ig_cache_key (images) then vs (videos).
    """
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    media_encoded = query.get("media", [None])[0]
    if media_encoded:
        media_url = urllib.parse.unquote(media_encoded)
        media_parsed = urllib.parse.urlparse(media_url)
        media_query = urllib.parse.parse_qs(media_parsed.query)

        ig_key = media_query.get("ig_cache_key", [None])[0]
        if ig_key:
            return f"img_{ig_key}"
        vs = media_query.get("vs", [None])[0]
        if vs:
            return f"vid_{vs}"
    return None


def fetch_html() -> str | None:
    """
    Calls the API endpoint and returns the 'html' field (or None on error).
    """
    try:
        resp = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and data.get("status") == "ok" and "html" in data:
            return data["html"]
    except requests.RequestException:
        pass
    except ValueError:
        # JSON decode error
        pass
    return None


def extract_media_links(html: str) -> dict[str, str]:
    """
    Parses the HTML and returns a dict[id] = media_url for all <img> and <video><source>.
    Mirrors your Selenium-based selection inside elements with class 'load'.
    """
    soup = BeautifulSoup(html, "html.parser")
    links: dict[str, str] = {}

    for load in soup.select(".load"):
        # Try image first
        img = load.find("img")
        if img and img.get("src"):
            media_url = img["src"]
            mid = get_id(media_url)
            if mid:
                links[mid] = media_url
            continue  # consistent with your original priority (img vs video)

        # Then try video
        video = load.find("video")
        if video:
            source = video.find("source")
            if source and source.get("src"):
                media_url = source["src"]
                mid = get_id(media_url)
                if mid:
                    links[mid] = media_url

    return links


def shorten(url: str) -> str | None:
    try:
        r = requests.get(TINYURL_API + urllib.parse.quote(url, safe=""), timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.text.strip()
    except requests.RequestException:
        return None


def load_existing() -> dict[str, str]:
    if os.path.exists(LINKS_DB):
        try:
            with open(LINKS_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_existing(data: dict[str, str]) -> None:
    try:
        with open(LINKS_DB, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def main():
    # while True:
        html = fetch_html()
        if html:
            found = extract_media_links(html)

            # Build short links for new IDs only
            existing = load_existing()
            new_short_links: list[str] = []

            for mid, media_url in found.items():
                if mid not in existing:
                    tiny = shorten(media_url) or media_url  # fall back to original if shortening fails
                    existing[mid] = tiny
                    new_short_links.append(tiny)

            # Notify only when there are new links
            if new_short_links:
                try:
                    send_telegram_message(new_short_links)
                except Exception:
                    # Keep running even if Telegram send fails
                    pass

            save_existing(existing)

        # time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
