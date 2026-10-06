import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime


# ============================================================
# ۱. اسکرپ ساده - عنوان و پاراگراف‌ها
# ============================================================
def scrape_headlines(url):
    """استخراج عنوان و پاراگراف‌های اصلی صفحه"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "lxml")

    result = {
        "title": soup.title.string if soup.title else "No title",
        "headings": [],
        "paragraphs": [],
    }

    for h in soup.find_all(["h1", "h2", "h3"]):
        text = h.get_text(strip=True)
        if text:
            result["headings"].append(text)

    for p in soup.find_all("p")[:10]:
        text = p.get_text(strip=True)
        if text and len(text) > 30:
            result["paragraphs"].append(text)

    return result


# ============================================================
# ۲. استخراج همه‌ی لینک‌ها
# ============================================================
def extract_links(url):
    """استخراج همه‌ی لینک‌های صفحه"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "lxml")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        # فقط لینک‌های خارجی
        if href.startswith("http"):
            links.append({"text": text, "url": href})

    return links[:20]


# ============================================================
# ۳. اسکرپ جدول (مثلاً لیگ فوتبال)
# ============================================================
def scrape_table(url):
    """استخراج داده‌های یه جدول HTML"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table")

    if not table:
        return {"error": "No table found"}

    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    return rows


# ============================================================
# ۴. اسکرپ با CSS Selector
# ============================================================
def scrape_by_selector(url, selector):
    """استخراج عناصر با CSS Selector"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "lxml")
    elements = soup.select(selector)

    results = []
    for el in elements[:15]:
        results.append({
            "tag": el.name,
            "text": el.get_text(strip=True)[:200],
            "class": el.get("class"),
        })
    return results


# ============================================================
# ۵. اسکرپ چند صفحه (Pagination)
# ============================================================
def scrape_quotes_pages(num_pages=3):
    """اسکرپ quoteها از quotes.toscrape.com (سایت تمرینی)"""
    all_quotes = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, num_pages + 1):
        url = f"http://quotes.toscrape.com/page/{page}/"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("div", class_="quote")

            for q in quotes:
                text = q.find("span", class_="text").get_text(strip=True)
                author = q.find("small", class_="author").get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]

                all_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags,
                })

            print(f"  ✅ Page {page} scraped ({len(quotes)} quotes)")
            time.sleep(1)  # احترام به سرور

        except Exception as e:
            print(f"  ❌ Error on page {page}: {e}")
            break

    return all_quotes


# ============================================================
# ۶. ذخیره‌ی نتایج توی فایل
# ============================================================
def save_to_json(data, filename):
    """ذخیره‌ی نتایج توی فایل JSON"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"💾 Saved to {filename}")
    except IOError as e:
        print(f"❌ Could not save: {e}")


# ============================================================
# منوی اصلی
# ============================================================
def main():
    print("=" * 50)
    print("🕷️  Web Scraper")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Scrape headlines from a URL")
        print("2. Extract links from a URL")
        print("3. Scrape a table")
        print("4. Scrape by CSS selector")
        print("5. Scrape quotes (multi-page demo)")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            url = input("URL: ").strip()
            result = scrape_headlines(url)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            url = input("URL: ").strip()
            links = extract_links(url)
            if isinstance(links, dict):
                print(links)
            else:
                for link in links:
                    print(f"  🔗 {link['text'][:50]:<50} → {link['url']}")

        elif choice == "3":
            url = input("URL with table: ").strip()
            rows = scrape_table(url)
            if isinstance(rows, dict):
                print(rows)
            else:
                for row in rows[:15]:
                    print(" | ".join(row))

        elif choice == "4":
            url = input("URL: ").strip()
            selector = input("CSS selector (e.g., h2.title): ").strip()
            results = scrape_by_selector(url, selector)
            print(json.dumps(results, indent=2, ensure_ascii=False))

        elif choice == "5":
            pages = int(input("How many pages? (1-10): ").strip())
            quotes = scrape_quotes_pages(pages)
            print(f"\n✅ Total: {len(quotes)} quotes")
            save_to_json(quotes, "quotes.json")

        elif choice == "6":
            print("Bye! 👋")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()